from sultan.core import Base
from sultan.echo import Echo

class Result(Base):
    """
    Class that encompasses the result of a POpen command.
    """

    def __init__(self, stdout, stderr, traceback=None):

        super(Result, self).__init__()        
        self.__stdout = stdout
        self.__stderr = stderr
        self.__traceback = traceback
        self.__echo = Echo()

    def __str__(self):

        return '\n'.join(self.__stdout)

    def __format_line(self, msg):

        return '| %s' % msg

    def __format_lines(self, lines):

        for line in lines:
            self.__echo.error(self.__format_line(line))

    @property
    def stdout(self):
        '''
        Converts stdout string to a list.
        '''
        return self.__stdout.strip().splitlines() if self.__stdout else ''

    @property
    def stderr(self):
        '''
        Converts stderr string to a list.
        '''
        return self.__stderr.strip().splitlines() if self.__stderr else ''

    @property
    def traceback(self):
        '''
        Converts traceback string to a list.
        '''
        return self.__traceback

    def print_stdout(self):
        '''
        Prints the stdout to console
        '''
        self.__echo.critical("--{ STDOUT }---" + "-" * 100)
        self.__format_lines(self.stdout)
        self.__echo.critical("---------------" + "-" * 100)

    def print_stderr(self):
        '''
        Prints the stderr to console
        '''
        self.__echo.critical("--{ STDERR }---" + "-" * 100)
        self.__format_lines(self.stderr)
        self.__echo.critical("---------------" + "-" * 100)

    def print_traceback(self):
        '''
        Prints the traceback to console
        '''
        self.__echo.critical("--{ TRACEBACK }" + "-" * 100)
        self.__format_lines(self.traceback)
        self.__echo.critical("---------------" + "-" * 100)


