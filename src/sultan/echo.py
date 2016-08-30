from .core import Base

class Echo(Base):

    def echo(self, msg):

        print msg

    def echo_cmd(self, msg):

        print msg

    def echo_error(self, msg):

        print msg