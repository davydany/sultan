import os
import subprocess
import traceback

from .core import Base
from .conf import Settings
from .echo import Echo

def shell_decorator(name):

    pass

class Sultan(Base):

    commands = []

    def __init__(self):

        self.commands = []
        self.__echo = Echo()
        self.settings = Settings()

    def __call__(self):

        if self.commands:

            # run commands
            self.run()

            # clear the commands buffer
            self.clear()

    def __getattr__(self, name):

        return Command(self, name)

    def run(self):

        commands = str(self)
        self.__echo.cmd(commands)
        try:
            response = subprocess.check_output(commands, shell=True)
            return response
        except Exception, e:
            
            self.__echo.error("Unable to run '%s'" % commands)
            self.__echo.error(traceback.format_exc())
            if self.settings.HALT_ON_ERROR:
                raise

    def add(self, command):

        self.commands.append(command)
        return self

    def clear(self):

        del self.commands[:]
        return self

    def __str__(self):

        SPECIAL_CASES = (Pipe, And, )
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
            
        return output.strip() + ";"

    def spit(self):

        self.__echo.log(str(self))

    def pipe(self):

        self.add(Pipe(self, '|'))
        return self

    def and_(self):

        self.add(And(self, "&&"))
        return self

class Command(Base):

    command = None
    args = []
    kwargs = {}

    def __init__(self, sultan, name):

        self.sultan = sultan
        self.command = name

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

        if len(kwargs) == 0 and len(args) == 1 and type(args[0]) == str:
            self.args = args[0].split(" ")
            self.sultan.add(self)
        else:
            self.args = args
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

class Pipe(Command):

    def __call__(self):

        pass # do nothing

    def __str__(self):
        return self.command

class And(Command):

    def __call__(self):

        pass # do nothing

    def __str__(self):

        return self.command

class Redirect(Command):

    def __call__(self, to_file, append=False, stdout=False, stderr=False):
        print to_file

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