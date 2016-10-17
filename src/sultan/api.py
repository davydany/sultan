__doc__ = """
Sultan is a Python package for interfacing with command-line utilities, like 
`yum`, `apt-get`, or `ls`, in a Pythonic manner. It lets you run command-line 
utilities using simple function calls. 

Here is how you'd use Sultan::

    from sultan.api import Sultan

    # simple way
    s = Sultan()
    s.sudo("yum install -y tree").run()

    # with context management (recommended)
    with Sultan.load(sudo=True) as s:
        s.yum("install -y tree").run()

What if we want to install this command on a remote machine? You can easily 
achieve this using context management::

    with open(sudo=True, hostname="myserver.com") as s:
        s.yum("install -y tree").run()

If you enter a wrong command, Sultan will print out details you need to debug and 
find the problem quickly.

Here, the same command was run on a Mac::

    In [1]: with Sultan.load(sudo=True) as s:
      ...:     s.yum("install -y tree").run()
      ...:
    [sultan]: sudo su - root -c 'yum install -y tree;'
    Password:
    [sultan]: Unable to run 'sudo su - root -c 'yum install -y tree;''
    [sultan]: --{ TRACEBACK }----------------------------------------------------------------------------------------------------
    [sultan]: | Traceback (most recent call last):
    [sultan]: |   File "/Users/davydany/projects/aeroxis/sultan/src/sultan/api.py", line 159, in run
    [sultan]: |     stdout = subprocess.check_output(commands, shell=True, stderr=stderr)
    [sultan]: |   File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 573, in check_output
    [sultan]: |     raise CalledProcessError(retcode, cmd, output=output)
    [sultan]: | CalledProcessError: Command 'sudo su - root -c 'yum install -y tree;'' returned non-zero exit status 127
    [sultan]: -------------------------------------------------------------------------------------------------------------------
    [sultan]: --{ STDERR }-------------------------------------------------------------------------------------------------------
    [sultan]: | -sh: yum: command not found
    [sultan]: -------------------------------------------------------------------------------------------------------------------

Want to get started? Simply install Sultan, and start writing your clean code::

    pip install --upgrade sultan

If you have more questions, check the docs! http://sultan.readthedocs.io/en/latest/
"""

import getpass
import os
import subprocess
import tempfile
import traceback

from .core import Base
from .config import Settings
from .err import InvalidContextError
from .echo import Echo

__all__ = ['Sultan']

class Sultan(Base):
    """
    The Pythonic interface to Bash.
    """
    commands = None
    _context = None
    
    @classmethod
    def load(cls, cwd=None, sudo=False, user=None, hostname=None, **kwargs):
        
        context = {}
        context['cwd'] = cwd
        context['sudo'] = sudo
        context['hostname'] = hostname

        # determine user
        if user:
            context['user'] = user
        else:
            context['user'] = 'root' if sudo else getpass.getuser()
        context.update(kwargs)

        s = Sultan(context=context)
        return s

    def __init__(self, context=None):

        self.commands = []
        self.__echo = Echo()
        self.settings = Settings()

        if context:
            if self._context:
                self._context.append(context)
            else:
                self._context = [context]
        else:
            self._context = []

    @property
    def current_context(self):
        """
        Returns the context that Sultan is running on
        """
        return self._context[-1] if len(self._context) > 0 else {}
        
    def __enter__(self):
        """
        Sultan can be used with context using `with` blocks, as such:

        ```python

        with Sultan.load(cwd="/tmp") as s:
            s.ls("-lah").run()
        ```

        This is easier to manage than doing the following::
        
            s = Sultan()
            s.cd("/tmp").and_().ls("-lah").run()

        There are one-off times when running `s.cd("/tmp").and_().ls("-lah").run()` works better. However, 
        if you have multiple commands to run in a given directory, using Sultan with context, allows your
        code to be easy to manage.
        """
        # do nothing since we got 'current_context' and '_context' are doing the work
        # however, we do want to alert the user that they're using contexts badly.
        if len(self._context) == 0:
            raise InvalidContextError("You're using the 'with' block to load Sultan, but didn't provide a context with 'Sultan.context(...)'")
        return self

    def __exit__(self, type, value, traceback):
        """
        Restores the context to previous context.
        """
        if len(self._context) > 0:
            self._context.pop()
        
    def __call__(self):
        
        if self.commands:

            # run commands
            self.run()

            # clear the commands buffer
            self.clear()

    def __getattr__(self, name):

        if name == "redirect":
            return Redirect(self, name)
        else:
            return Command(self, name)

    def run(self, halt_on_nonzero=True):
        """
        After building your commands, call `run()` to have your code executed.
        """
        def format_lines(lines):
            for line in lines:
                self.__echo.error(format_line(line))

        def format_line(msg):
            return "| %s" % msg

        commands = str(self)
        self.__echo.cmd(commands)

        stdout, stderr = None, None
        try:
            stdout, stderr = subprocess.Popen(commands, 
                shell=True, 
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE).communicate()

            # stdout = subprocess.check_output(commands, shell=True, stderr=stderr)
            response = stdout.strip().split("\n") if stdout else stdout
            return response
        except Exception, e:
            tb = traceback.format_exc().strip().split("\n")
            
            self.__echo.critical("Unable to run '%s'" % commands)

            #traceback
            self.__echo.critical("--{ TRACEBACK }" + "-" * 100)
            format_lines(tb)
            self.__echo.critical("---------------" + "-" * 100)

            # standard out
            if stdout:
                self.__echo.critical("--{ STDOUT }---" + "-" * 100)
                format_lines(stdout)
                self.__echo.critical("---------------" + "-" * 100)

            # standard error
            if stderr:
                self.__echo.critical("--{ STDERR }---" + "-" * 100)
                format_lines(stderr)
                self.__echo.critical("---------------" + "-" * 100)
            
            if self.settings.HALT_ON_ERROR:
                if halt_on_nonzero:
                    raise

            if halt_on_nonzero:
                raise

        finally:
            
            # clear the buffer
            self.clear()

    def _add(self, command):
        """
        Private method that adds a custom command (see `pipe` and `and_`).
        
        NOT FOR PUBLIC USE 
        """
        self.commands.append(command)
        return self

    def clear(self):

        del self.commands[:]
        return self

    def __str__(self):
        """
        Returns the chained commands that were built as a string.
        """
        context = self.current_context
        SPECIAL_CASES = (Pipe, And, Redirect)
        output = ""
        for i, cmd in enumerate(self.commands):

            if (i == 0):
                separator = ""
            else:
                if type(cmd) in SPECIAL_CASES:
                    separator = " "
                else:
                    if type(self.commands[i-1]) in SPECIAL_CASES:
                        separator = " "
                    else:
                        separator = "; "

            cmd_str = str(cmd)
            output += separator + cmd_str
            
        output = output.strip() + ";"

        # update with 'cwd' context
        cwd = context.get('cwd')
        if cwd:
            prepend = "cd %s && " % (cwd)
            output = prepend + output
        
        # update with 'sudo' context
        sudo = context.get('sudo')
        user = context.get('user')
        hostname = context.get('hostname')
        if sudo:
            output = "sudo su - %s -c '%s'" % (user, output)

        if hostname:
            params = {
                'user': user,
                'hostname': hostname,
                'command': output
            }
            output = "ssh %(user)s@%(hostname)s '%(command)s'" % (params)
        
        return output

    def spit(self):
        """
        Logs to the logger the command.
        """
        self.__echo.log(str(self))

    def pipe(self):
        """
        Pipe commands in Sultan.

        Usage::

            # runs: 'cat /var/log/foobar.log | grep 192.168.1.1'
            s = Sultan()
            s.cat("/var/log/foobar.log").pipe().grep("192.168.1.1").run()
        """
        self._add(Pipe(self, '|'))
        return self

    def and_(self):
        """
        Combines multiple commands using `&&`.

        Usage::

            # runs: 'cd /tmp && touch foobar.txt'
            s = Sultan()
            s.cd("/tmp").and_().touch("foobar.txt").run()
        """
        self._add(And(self, "&&"))
        return self

    def stdin(self, message):

        return raw_input(message)

    
class BaseCommand(Base):
    """
    The Base class for all commands.
    """

    command = None
    args = None
    kwargs = None
    context = None

    def __init__(self, sultan, name, context=None):

        self.sultan = sultan
        self.command = name
        self.args = []
        self.kwargs = {}
        self.context = context if context else {}

class Command(BaseCommand):
    """
    The class that all commands are based off. Essentially, when we run 
    `Sultan().foo()`, `foo` is represented as an instance of `Command`.

    """
    def __call__(self, *args, **kwargs):

        # check for 'where' in kwargs
        if 'where' in kwargs:
            where = kwargs.pop('where')
            if not os.path.exists(where):
                raise IOError("The value for 'where' (%s), for '%s' does not exist." % (where, self.command))
            
            cmd = os.path.join(where, self.command)
            if not os.path.exists(cmd):
                raise IOError("Command '%s' does not exist in '%s'." % (cmd, where))

            self.command = os.path.join(where, cmd)
        
        if "sudo" in kwargs:
            sudo = kwargs.pop("sudo")
            self.command = "sudo " + self.command

        self.args = [str(a) for a in args]
        self.kwargs = kwargs
        self.sultan._add(self)
        return self.sultan

    def __str__(self):

        args_str = (" ".join(self.args)).strip()
        kwargs_list = []
        for k, v in self.kwargs.iteritems():

            key = None
            value = v
            if len(k) == 1:
                key = "-%s" % k
            else:
                key = "--%s" % k
            kwargs_list.append("%s=%s" % (key, value))
        kwargs_str = " ".join(kwargs_list).strip()

        # prep and return the output
        output = self.command
        if len(kwargs_str) > 0: output = output + " " + kwargs_str
        if len(args_str) > 0: output = output + " " + args_str
        
        return output

class Pipe(BaseCommand):
    """
    Representation of the Pipe `|` operator.
    """
    def __call__(self):

        pass # do nothing

    def __str__(self):
        
        return self.command

class And(BaseCommand):
    """
    Representation of the And `&&` operator.
    """
    def __call__(self):

        pass # do nothing

    def __str__(self):

        return self.command

class Redirect(BaseCommand):
    """
    Representation of the Redirect (`>`, `>>`, ...) operator.
    """
    def __call__(self, to_file, append=False, stdout=False, stderr=False):
        
        descriptor = None
        if stdout and stderr:
            descriptor = "&"
        else:
            if stdout and not stderr:
                descriptor = "1"
            elif stderr and not stdout:
                descriptor = "2"
            else:
                raise ValueError("You chose redirect to stdout and stderr to be false. This is not valid.")
        
        descriptor = descriptor + ">" + (">" if append else "")
        self.command = "%s %s" % (descriptor, to_file)
        self.sultan._add(self)
        return self.sultan

    def __str__(self):

        return self.command