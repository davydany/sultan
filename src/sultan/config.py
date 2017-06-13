import os
from .core import Base

DEFAULT_SETTINGS = {
    "HALT_ON_ERROR": True,
    "LOG_FORMAT": '%(log_color)s[%(name)s]: %(message)s',
    "LOG_COLORS": {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
}


SULTAN_SETTINGS_MODULE_ENV = 'SULTAN_SETTINGS_MODULE'


class Settings(Base):

    def __init__(self):
        super(Settings, self).__init__()
        self._settings = DEFAULT_SETTINGS.copy()
        self._load_setting_module()

    def _load_setting_module(self):
        if SULTAN_SETTINGS_MODULE_ENV in os.environ:
            settings = __import__(os.environ[SULTAN_SETTINGS_MODULE_ENV])
            for k, v in settings.items():
                self._settings[k] = v

    def __getattr__(self, attr):
        try:
            return self._settings[attr]
        except KeyError:
            raise ValueError("Invalid Setting '%s'." % (attr))


settings = Settings()
