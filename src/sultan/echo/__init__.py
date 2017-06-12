import logging
from sultan.core import Base
from sultan.echo.colorlog import StreamHandler, ColoredFormatter
from sultan.config import settings

handler = StreamHandler()
handler.setFormatter(ColoredFormatter(
    settings.LOG_FORMAT,
    log_colors=settings.LOG_COLORS
))


def getLogger(name='', level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


class Echo(Base):

    def __init__(self, activated=True):

        self.logger = getLogger(name='sultan')
        self.activated = activated

    def log(self, msg):

        if self.activated:
            self.logger.info(msg)

    def cmd(self, msg):

        if self.activated:
            self.logger.debug(msg)

    def stdout(self, msg):

        if self.activated:
            self.logger.info(msg)

    def stderr(self, msg):

        if self.activated:
            self.logger.critical(msg)

    def debug(self, msg):

        if self.activated:
            self.logger.debug(msg)

    def info(self, msg):

        if self.activated:
            self.logger.info(msg)

    def warn(self, msg):

        if self.activated:
            self.logger.warning(msg)

    def error(self, msg):

        if self.activated:
            self.logger.error(msg)

    def critical(self, msg):

        if self.activated:
            self.logger.critical(msg)
