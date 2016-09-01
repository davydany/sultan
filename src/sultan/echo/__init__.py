import logging
from sultan.core import Base
from sultan.echo.colorlog import StreamHandler, ColoredFormatter

handler = StreamHandler()
handler.setFormatter(ColoredFormatter(
    '%(log_color)s[sultan]  %(message)s'
))

logger = logging.getLogger('sultan')
logger.addHandler(handler)


class Echo(Base):

    def log(self, msg):

        logger.info(msg)

    def cmd(self, msg):

        logger.debug(msg)

    def stdout(self, msg):

        logger.info(msg)

    def stderr(self, msg):

        logger.critical(msg)

    def debug(self, msg):

        logger.debug(msg)

    def info(self, msg):

        logger.info(msg)

    def warn(self, msg):

        logger.warning(msg)

    def error(self, msg):

        logger.error(msg)

    def critical(self, msg):

        logger.critical(msg)