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

    def __init__(self):

        self.logger = getLogger(name='sultan')

    def log(self, msg):

        self.logger.info(msg)

    def cmd(self, msg):

        self.logger.debug(msg)

    def stdout(self, msg):

        self.logger.info(msg)

    def stderr(self, msg):

        self.logger.critical(msg)

    def debug(self, msg):

        self.logger.debug(msg)

    def info(self, msg):

        self.logger.info(msg)

    def warn(self, msg):

        self.logger.warning(msg)

    def error(self, msg):

        self.logger.error(msg)

    def critical(self, msg):

        self.logger.critical(msg)