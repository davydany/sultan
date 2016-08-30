from .core import Base

class Colorizer:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHT_PURPLE = '\033[94m'
    PURPLE = '\033[95m'
    END = '\033[0m'

    @classmethod
    def red(cls, s):
        print(cls.RED + s + cls.END)

    @classmethod
    def green(cls, s):
        print(cls.GREEN + s + cls.END)

    @classmethod
    def yellow(cls, s):
        print(cls.YELLOW + s + cls.END)

    @classmethod
    def lightPurple(cls, s):
        print(cls.LIGHT_PURPLE + s + cls.END)

    @classmethod
    def purple(cls, s):
        print(cls.PURPLE + s + cls.END)

class Echo(Base):

    def log(self, msg):

        print Colorizer.green(msg)

    def cmd(self, msg):

        print Colorizer.purple(msg)

    def error(self, msg):

        print Colorizer.red(msg)