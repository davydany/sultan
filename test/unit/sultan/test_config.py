import unittest
from sultan.config import Settings


class TestSettings(unittest.TestCase):

    def setUp(self):

        self.settings = Settings()

    def test_default_settings_loaded(self):

        self.assertEqual(self.settings.HALT_ON_ERROR, True)

    def test_log_format(self):

        self.assertEqual(self.settings.LOG_FORMAT, '%(log_color)s[%(name)s]: %(message)s')

    def test_log_colors(self):

        self.assertEqual(self.settings.LOG_COLORS, {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        })