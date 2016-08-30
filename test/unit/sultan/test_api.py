import os
import unittest
from sultan import api


class SultanTestCase(unittest.TestCase):

    def test_basic_command_chains(self):

        sultan = api.Sultan()
        self.assertEqual(str(sultan.touch("/tmp/foo").ls("-1 /tmp/foo").whoami()), "touch /tmp/foo; ls -1 /tmp/foo; whoami;")

    def test_command_generation(self):

        sultan = api.Sultan()
        self.assertEqual(str(sultan.yum("install", "gcc")), "yum install gcc;")

        sultan = api.Sultan()
        self.assertEqual(str(sultan.yum("install", "-y", "gcc")), "yum install -y gcc;")

        sultan = api.Sultan()
        self.assertEqual(str(sultan.yum("install -y gcc")), "yum install -y gcc;")


    def test_command_generation_for_chains(self):

        sultan = api.Sultan()
        self.assertEqual(str(sultan.touch("/tmp/foo").and_().touch("/tmp/bar")), "touch /tmp/foo && touch /tmp/bar;")

        sultan = api.Sultan()
        self.assertEqual(
            str(sultan.yum("install -y gcc").and_().ls("-lah /tmp").and_().find("/ -name gcc")),
            "yum install -y gcc && ls -lah /tmp && find / -name gcc;"
        )

    def test_execution(self):
    
        sultan = api.Sultan()
        sultan.touch("/tmp/foo").run()
        response = sultan.ls("-1 /tmp/foo").run()
        self.assertEqual(response, "/tmp/foo\n")

    # def test_execution_with_chains(self):

    #     sultan = api.Sultan()
    #     sultan.echo("""'
    #     Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
    #     Maecenas sagittis et mauris at viverra. 
    #     Duis tincidunt semper tortor vel iaculis.' 
    #     """).run()

    #     raise "Foo"

    def test_and(self):

        sultan = api.Sultan()
        self.assertEqual(str(sultan.touch("/tmp/foo").and_().touch("/tmp/bar")), "touch /tmp/foo && touch /tmp/bar;")

class SultanCommandTestCase(unittest.TestCase):

    def test_normal(self):

        sultan = api.Sultan()
        command = api.Command(sultan, "yum")
        self.assertEqual(str(command), "yum")

    def test_where_attribute(self):

        sultan = api.Sultan()
        command = api.Command(sultan, "df")
        self.assertEqual(str(command(where="/bin")), "/bin/df;")

class PipeTestCase(unittest.TestCase):

    def test_pipe(self):

        s = api.Sultan()
        r = api.Redirect(s, '|')
        self.assertEqual(r.command, "|")
        self.assertEqual(str(r.command), "|")

class AndTestCase(unittest.TestCase):

    def test_and(self):

        s = api.Sultan()
        r = api.Redirect(s, '&')
        self.assertEqual(r.command, "&")
        self.assertEqual(str(r.command), "&")

class TestRedirect(unittest.TestCase):

    def test_redirect_stdout_only(self):

        s = api.Sultan()
        r = api.Redirect(s, '')
        r("/tmp/foo", stdout=True)
        self.assertEqual(r.command, "1> /tmp/foo")

    def test_redirect_stderr_only(self):

        s = api.Sultan()
        r = api.Redirect(s, '')
        r("/tmp/foo", stderr=True)
        self.assertEqual(r.command, "2> /tmp/foo")

    def test_redirect_stdout_only_with_append(self):

        s = api.Sultan()
        r = api.Redirect(s, '')
        r("/tmp/foo", stdout=True, append=True)
        self.assertEqual(r.command, "1>> /tmp/foo")

    def test_redirect_stderr_only_with_append(self):

        s = api.Sultan()
        r = api.Redirect(s, '')
        r("/tmp/foo", stderr=True, append=True)
        self.assertEqual(r.command, "2>> /tmp/foo")

    def test_redirect_stdout_and_stderr(self):

        s = api.Sultan()
        r = api.Redirect(s, '')
        r("/tmp/foo", stdout=True, stderr=True)
        self.assertEqual(r.command, "&> /tmp/foo")

    def test_redirect_stdout_and_stderr_with_append(self):

        s = api.Sultan()
        r = api.Redirect(s, '')
        r("/tmp/foo", stdout=True, stderr=True, append=True)
        self.assertEqual(r.command, "&>> /tmp/foo")