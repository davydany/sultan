import unittest
from sultan import api


class TestSultan(unittest.TestCase):

    def setUp(self):

        self.sultan = api.Sultan()


    def test_commands_populated(self):

        self.assertEqual(str(self.sultan.yum("install", "gcc")), "yum install gcc")
        self.sultan.clear()
        self.assertEqual(str(self.sultan.yum("install", "-y", "gcc")), "yum install -y gcc")
        self.sultan.clear()
        self.assertEqual(str(self.sultan.yum("install -y gcc")), "yum install -y gcc")
        self.sultan.clear()