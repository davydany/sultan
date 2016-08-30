import unittest
from sultan import api


class TestSultan(unittest.TestCase):

    def setUp(self):

        self.sultan = api.Sultan()

    def test_command_joins(self):

        self.assertEqual(str(self.sultan.touch("/tmp/foo").ls("-1 /tmp/foo").whoami()), "touch /tmp/foo; ls -1 /tmp/foo; whoami;")
        self.sultan.clear()

    def test_commands_populated(self):

        self.sultan.clear()
        self.assertEqual(str(self.sultan.yum("install", "gcc")), "yum install gcc;")
        self.sultan.clear()
        self.assertEqual(str(self.sultan.yum("install", "-y", "gcc")), "yum install -y gcc;")
        self.sultan.clear()
        self.assertEqual(str(self.sultan.yum("install -y gcc")), "yum install -y gcc;")
        self.sultan.clear()

    def test_execution(self):

        self.sultan.clear()
        self.sultan.touch("/tmp/foo").run()
        response = self.sultan.ls("-1 /tmp/foo").run()
        self.assertEqual(response, "/tmp/foo\n")