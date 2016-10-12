__doc__ = """
# Sultan API

Sultan provides a pythonic interface to bash. Run bash commands like you'd 
normally run a python method, and Sultan will automatically use the 
'subprocess' API to write your command, and return your results. 

"""

import os
import subprocess
import traceback

from .core import Base
from .conf import Settings
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
    def load(cls, cwd=None, **kwargs):
        
        context = {}
        context['cwd'] = cwd
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

        This is easier to manage than doing the following:

        ```python
        
        s = Sultan()
        s.cd("/tmp").and_().ls("-lah").run()
        ```

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
        commands = str(self)
        self.__echo.cmd(commands)
        try:
            stdout = subprocess.check_output(commands, shell=True)
            response = stdout.strip().split("\n") if stdout else stdout
            return response
        except Exception, e:
            
            self.__echo.error("Unable to run '%s'" % commands)
            tb = traceback.format_exc().split("\n")
            for l in tb:
                self.__echo.critical("    %s" % l)
            if self.settings.HALT_ON_ERROR:
                if halt_on_nonzero:
                    raise
        finally:
            
            # clear the buffer
            self.clear()

    def _add(self, command):
        """
        Private method that adds a custom command (see `pipe` and `and_`). 
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
        
        return output

    def spit(self):
        """
        Logs to the logger the command.
        """
        self.__echo.log(str(self))

    def pipe(self):
        """
        Pipe commands in Sultan.

        Usage:

        ```
        s = Sultan()
        s.cat("/var/log/foobar.log").pipe().grep("192.168.1.1").run()
        ```
        """
        self._add(Pipe(self, '|'))
        return self

    def and_(self):
        """
        Combines multiple commands using `&&`.

        Usage:

        ```
        s = Sultan()
        s.cd("/tmp").and_().touch("foobar.txt").run()
        ```
        """
        self._add(And(self, "&&"))
        return self

    
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
        self.sultan.add(self)
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
        self.sultan.add(self)
        return self.sultan

    def __str__(self):

        return self.command