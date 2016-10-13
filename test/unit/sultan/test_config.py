import unittest
from sultan.config import Settings


class TestSettings(unittest.TestCase):

    def setUp(self):

        self.settings = Settings()

    def test_default_settings_loaded(self):

        self.assertEqual(self.settings.HALT_ON_ERROR, True)