"""
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
import sys

from .core import Base
from .config import Settings
from .echo import Echo
from .exceptions import InvalidContextError
from .result import Result

__all__ = ['Sultan']

if sys.version_info < (3, 0):
    input = raw_input


class Sultan(Base):
    """
    The Pythonic interface to Bash.
    """

    @classmethod
    def load(cls, 
        cwd=None, sudo=False, user=None, 
        hostname=None, env=None, logging=True,
        executable=None,
        ssh_config=None, src=None, 
        **kwargs):

        # initial checks
        if ssh_config and not isinstance(ssh_config, SSHConfig):
            msg = "The config passed (%s) must be an instance of SSHConfig." % \
                ssh_config
            raise ValueError(msg)

        if src and not os.path.exists(src):
            raise IOError("The Source File provided (%s) does not exist" % src)

        if executable and not os.path.exists(executable):
            raise IOError("The set Executable (%s) does not exist" % src)

        context = {}
        context['cwd'] = cwd
        context['sudo'] = sudo
        context['hostname'] = hostname
        context['ssh_config'] = str(ssh_config) if ssh_config else ''
        context['env'] = env or None # must be None, for Python to get the current process's env.
        context['logging'] = logging
        context['src'] = src
        context['executable'] = executable

        # determine user
        if user:
            context['user'] = user
        else:
            context['user'] = getpass.getuser()
        context.update(kwargs)

        return cls(context=context)

    def __init__(self, context=None):

        self.commands = []
        self._context = [context] if context is not None else []
        self.logging_activated = context.get('logging') if context else False
        self._echo = Echo(activated=self.logging_activated)
        self.settings = Settings()

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
            # When calling Bash Commands from Python with Sultan, we encounter
            # an issue where the Python doesn't allow special characters like 
            # dashes (i.e.: apt-get). To get around this, we will use 2 
            # underscores one after another to indicate that we want it to be a
            # dash, and replace it accordingly before calling Command
            name = name.replace('__', '-')

            # call Command()
            return Command(self, name)

    def exc(self, command, halt_on_nonzero=True, quiet=False, q=False, streaming=False):

        self.commands = command.split(' ')
        return self.run(halt_on_nonzero=halt_on_nonzero, quiet=quiet, q=q, streaming=streaming)

    def run(self, halt_on_nonzero=True, quiet=False, q=False, streaming=False):
        """
        After building your commands, call `run()` to have your code executed.
        """
        commands = str(self)
        if not (quiet or q):
            self._echo.cmd(commands)

        env = self._context[0].get('env', {}) if len(self._context) > 0 else os.environ
        executable = self.current_context.get('executable')
        try:
            process = subprocess.Popen(commands,
                                       bufsize=1,
                                       shell=True,
                                       env=env,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       executable=executable,
                                       universal_newlines=True)
            result = Result(process, commands, self._context, streaming, halt_on_nonzero=halt_on_nonzero)

        except Exception as e:
            result = Result(None, commands, self._context, exception=e)
            result.dump_exception()
            if halt_on_nonzero:
                raise e
        
        return result

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
        SPECIAL_CASES = (Pipe, And, Redirect, Or)
        output = ""
        for i, cmd in enumerate(self.commands):

            if (i == 0):
                separator = ""
            else:
                if isinstance(cmd, SPECIAL_CASES):
                    separator = " "
                else:
                    if isinstance(self.commands[i - 1], SPECIAL_CASES):
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

        # update with 'src' context
        src = context.get('src')
        if src:
            prepend = "source %s && " % (src)
            output = prepend + output

        # update with 'sudo' context
        sudo = context.get('sudo')
        user = context.get('user')
        if sudo:
            if user != getpass.getuser():
                output = "sudo su - %s -c '%s'" % (user, output)
            elif getpass.getuser() == 'root':
                output = "su - %s -c '%s'" % (user, output)
            else:
                output = "sudo %s" % (output)

        # if we have to ssh, prepare for the SSH command
        ssh_config = context.get('ssh_config')
        hostname = context.get('hostname')
        if hostname:
            params = {
                'user': user,
                'hostname': hostname,
                'command': output, 
                'ssh_config': ' %s ' % ssh_config if ssh_config else ' '
            }
            output = "ssh%(ssh_config)s%(user)s@%(hostname)s '%(command)s'" % (params)

        return output

    def spit(self):
        """
        Logs to the logger the command.
        """
        self._echo.log(str(self))

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

    def or_(self):
        """
        Combines multiple commands using `||`.

        Usage::

            # runs: 'touch /tmp/foobar || echo "Step Completed"'
            s = Sultan()
            s.touch('/tmp/foobar').or_().echo("Step Completed").run()
        """
        self._add(Or(self, '||'))
        return self

    def stdin(self, message):

        return input(message)
    

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
            kwargs.pop("sudo")
            self.command = "sudo " + self.command

        self.args = [str(a) for a in args]
        self.kwargs = kwargs
        self.sultan._add(self)
        return self.sultan

    def __str__(self):

        args_str = (" ".join(self.args)).strip()
        kwargs_list = []
        for k, v in self.kwargs.items():
            value = v
            if len(k) == 1:
                key = "-%s" % k
            else:
                key = "--%s" % k
            kwargs_list.append("%s=%s" % (key, value))
        kwargs_str = " ".join(kwargs_list).strip()

        # prep and return the output
        output = self.command
        if len(kwargs_str) > 0:
            output += " " + kwargs_str
        if len(args_str) > 0:
            output += " " + args_str

        return output


class Pipe(BaseCommand):
    """
    Representation of the Pipe `|` operator.
    """
    def __call__(self):

        pass  # do nothing

    def __str__(self):

        return self.command


class And(BaseCommand):
    """
    Representation of the And `&&` operator.
    """
    def __call__(self):

        pass  # do nothing

    def __str__(self):

        return self.command


class Or(BaseCommand):
    """
    Representation of the Or `||` operator.
    """
    def __call__(self):

        pass  # do nothing

    def __str__(self):

        return self.command


class Redirect(BaseCommand):
    """
    Representation of the Redirect (`>`, `>>`, ...) operator.
    """
    def __call__(self, to_file, append=False, stdout=False, stderr=False):
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

class Config(object):

    params_map = {}

    def __init__(self, **config):

        self.config = config or {}
        self.validate_config()

    def __str__(self):

        output = []
        for key, value in self.config.items():

            shorthand = self.params_map[key]['shorthand']
            output.append(shorthand)
            output.append(str(value))
            
        return ' '.join(output)

    def validate_config(self):
        '''
        Validates the provided config to make sure all the required fields are 
        there.
        '''
        # first ensure that all the required fields are there
        for key, key_config in self.params_map.items():
            if key_config['required']:
                if key not in self.config:
                    raise ValueError("Invalid Configuration! Required parameter '%s' was not provided to Sultan.")
        
        # second ensure that the fields that were pased were actually fields that
        # can be used
        for key in self.config.keys():
            if key not in self.params_map:
                raise ValueError("Invalid Configuration! The parameter '%s' provided is not used by Sultan!" % key)



class SSHConfig(Config):

    params_map = {
        'identity_file': {
            'shorthand': '-i',
            'required': False
        },
        'port': {
            'shorthand': '-p',
            'required': False
        },
    }