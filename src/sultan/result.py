import sys

from Queue import Queue
from sultan.core import Base
from sultan.echo import Echo
from threading import Thread


def read_output(pipe, q):
    for line in iter(pipe.readline, b''):
        q.put(line.strip())
    pipe.close()


def write_input(pipe, q):
    for line in iter(q.get, None):
        pipe.write(line)
    

class Result(Base):
    """
    Class that encompasses the result of a POpen command.
    """

    def __init__(self, process, commands, context, streaming=False, traceback=''):
        super(Result, self).__init__()
        self._process = process
        self._commands = commands
        self._context = context
        self.__traceback = traceback
        self.__echo = Echo()
        self._streaming = streaming
        self.rc = None
        
        if process and streaming:
            self.is_complete = False
            self.__stdout = Queue()
            self.__stderr = Queue()
            self.__stdin = Queue()

            self._stdout_t = Thread(target=read_output, args=(process.stdout, self.__stdout))
            self._stderr_t = Thread(target=read_output, args=(process.stderr, self.__stderr))
            self._stdin_t = Thread(target=write_input, args=(process.stdin, self.__stdin))
            self._wait_t = Thread(target=self.wait_on_process)

            for t in (self._stdout_t, self._stderr_t, self._stdin_t, self._wait_t):
                t.daemon = True
                t.start()

        else:
            self.is_complete = True
            try:
                stdout, stderr = process.communicate()
            except:
                pass
                
            try:
                self.rc = process.returncode
            except:
                pass
                
            self.__stdout = stdout.strip().splitlines() if stdout else []
            self.__stderr = stderr.strip().splitlines() if stderr else []

    def wait_on_process(self):
        self.rc = self._process.wait()
        self.__stdin.put(None)
        self.is_complete = True
        for t in (self._stdout_t, self._stderr_t, self._stdin_t):
            t.join()
        sys.exit()
                
    def __display_exception_debug_information(self):

        def echo_debug_info(key):
            if self._context and len(self._context) > 0:
                self.__echo.warn("\t - %s: %s" % (key, self._context[0].get(key, 'N/A')))

        self.__echo.warn("The following are additional information that can be used to debug this exception.")
        self.__echo.warn("The following is the context used to run:")
        echo_debug_info('cwd')
        echo_debug_info('sudo')
        echo_debug_info('user')
        echo_debug_info('hostname')
        echo_debug_info('env')
        echo_debug_info('logging')
        echo_debug_info('executable')
        echo_debug_info('ssh_config')
        echo_debug_info('src')
        
    def __str__(self):
        return '\n'.join(self.stdout)

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
        if self._streaming:
            stdout = []
            while not self.__stdout.empty():
                try:
                    line = self.__stdout.get_nowait()
                    stdout.append(line)
                except:
                    pass
        else:
            stdout =  self.__stdout
        return stdout

    @property
    def stderr(self):
        """
        Converts stderr string to a list.
        """
        if self._streaming:
            stderr = []
            while not self.__stderr.empty():
                try:
                    line = self.__stderr.get_nowait()
                    stderr.append(line)
                except:
                    pass
        else:
            stderr = self.__stderr
        return stderr

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
        return self.is_complete and self.rc == 0

    @property
    def is_failure(self):
        """
        Returns if the result of the command was a failure.
        True for failure, False for succes.
        """
        return self.is_complete and not self.rc == 0

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
        if self.__stdout or always_print:
            self.__echo.info("--{ STDOUT }---" + "-" * 100)
            self.__format_lines_info(self.stdout)
            self.__echo.info("---------------" + "-" * 100)

    def print_stderr(self, always_print=False):
        """
        Prints the stderr to console - if there is any stdout, otherwise does nothing.
        :param always_print:   print the stderr, even if there is nothing in the buffer (default: false)
        """
        if self.__stderr or always_print:
            self.__echo.critical("--{ STDERR }---" + "-" * 100)
            self.__format_lines_error(self.stderr)
            self.__echo.critical("---------------" + "-" * 100)

    def print_traceback(self, always_print=False):
        """
        Prints the traceback to console - if there is any traceback, otherwise does nothing.
        :param always_print:   print the traceback, even if there is nothing in the buffer (default: false)
        """
        if self.__traceback or always_print:
            self.__echo.critical("--{ TRACEBACK }" + "-" * 100)
            self.__format_lines_error(self.traceback)
            self.__echo.critical("---------------" + "-" * 100)
