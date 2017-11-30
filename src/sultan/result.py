from sultan.core import Base
from sultan.echo import Echo


class Result(Base):
    """
    Class that encompasses the result of a POpen command.
    """

    def __init__(self, stdout, stderr, traceback=None, rc=None):

        super(Result, self).__init__()        
        self.__stdout = stdout
        self.__stderr = stderr
        self.__traceback = traceback
        self.rc = rc
        self.__echo = Echo()

    def __str__(self):

        return '\n'.join(self.__stdout)

    def __format_line(self, msg):

        return '| %s' % msg

    def __format_lines_error(self, lines):

        for line in lines:
            self.__echo.critical(self.__format_line(line))

    def __format_lines_info(self, lines):

        for line in lines:
            self.__echo.info(self.__format_line(line))

    @property
    def stdout(self):
        """
        Converts stdout string to a list.
        """
        return self.__stdout.strip().splitlines() if self.__stdout else ''

    @property
    def stderr(self):
        """
        Converts stderr string to a list.
        """
        return self.__stderr.strip().splitlines() if self.__stderr else ''

    @property
    def traceback(self):
        """
        Converts traceback string to a list.
        """
        return self.__traceback

    @property
    def is_success(self):
        """
        Returns if the result of the command was a success.
        True for success, False for failure.
        """
        return self.rc == 0

    @property
    def is_failure(self):
        """
        Returns if the result of the command was a failure.
        True for failure, False for succes.

        This is an inverse of self.is_success.
        """
        return not self.is_success

    @property
    def has_exception(self):
        '''
        Returns True if self.__traceback is not empty.
        '''
        return bool(self.__traceback)


    def print_stdout(self, always_print=False):
        """
        Prints the stdout to console - if there is any stdout, otherwise does nothing.
        :param always_print:   print the stdout, even if there is nothing in the buffer (default: false)
        """
        if self.stdout or always_print:
            self.__echo.info("--{ STDOUT }---" + "-" * 100)
            self.__format_lines_info(self.stdout)
            self.__echo.info("---------------" + "-" * 100)

    def print_stderr(self, always_print=False):
        """
        Prints the stderr to console - if there is any stdout, otherwise does nothing.
        :param always_print:   print the stderr, even if there is nothing in the buffer (default: false)
        """
        if self.stderr or always_print:
            self.__echo.critical("--{ STDERR }---" + "-" * 100)
            self.__format_lines_error(self.stderr)
            self.__echo.critical("---------------" + "-" * 100)

    def print_traceback(self, always_print=False):
        """
        Prints the traceback to console - if there is any traceback, otherwise does nothing.
        :param always_print:   print the traceback, even if there is nothing in the buffer (default: false)
        """
        if self.traceback or always_print:
            self.__echo.critical("--{ TRACEBACK }" + "-" * 100)
            self.__format_lines_error(self.traceback)
            self.__echo.critical("---------------" + "-" * 100)


