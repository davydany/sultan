import unittest
from sultan import api


class TestSultan(unittest.TestCase):

    def setUp(self):

        sultan = api.Sultan()

    def test_command_joins(self):

        sultan = api.Sultan()
        self.assertEqual(str(sultan.touch("/tmp/foo").ls("-1 /tmp/foo").whoami()), "touch /tmp/foo; ls -1 /tmp/foo; whoami;")

    def test_commands_populated(self):

        sultan = api.Sultan()
        self.assertEqual(str(sultan.yum("install", "gcc")), "yum install gcc;")
        sultan = api.Sultan()
        self.assertEqual(str(sultan.yum("install", "-y", "gcc")), "yum install -y gcc;")
        sultan = api.Sultan()
        self.assertEqual(str(sultan.yum("install -y gcc")), "yum install -y gcc;")
        sultan = api.Sultan()

    def test_execution(self):

        sultan = api.Sultan()
        sultan.touch("/tmp/foo").run()
        response = sultan.ls("-1 /tmp/foo").run()
        self.assertEqual(response, "/tmp/foo\n")

    def test_and(self):

        sultan = api.Sultan()
        self.assertEqual(str(sultan.touch("/tmp/foo").and_().touch("/tmp/bar")), "touch /tmp/foo && touch /tmp/bar;")
