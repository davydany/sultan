import mock
import os
import shutil
import subprocess
import unittest
import getpass

from sultan.api import And, Command, Pipe, Redirect, Sultan
from sultan.config import Settings
from sultan.echo import Echo
from sultan.err import InvalidContextError


class SultanTestCase(unittest.TestCase):

    def test_construction(self):

        sultan = Sultan()
        self.assertEqual(sultan.commands, [])
        self.assertTrue(isinstance(sultan.settings, Settings))

    def test_getattr(self):

        sultan = Sultan()
        self.assertTrue(isinstance(sultan.redirect, Redirect))
        self.assertTrue(isinstance(sultan.foobar, Command))

    @mock.patch("sultan.api.subprocess")
    def test_run_basic(self, m_subprocess):

        m_subprocess.check_output.return_value = "sample_response"
        sultan = Sultan()
        response = sultan.ls("-lah /tmp").run()
        self.assertTrue(m_subprocess.check_output.called)
        self.assertEqual(response, ["sample_response"])

    def test_run_advanced(self):

        sultan = Sultan()
        try:
            sultan.mkdir("-p /tmp/mytestdir")\
                .mkdir("-p /tmp/mytestdir/foobar")\
                .touch("/tmp/mytestdir/a")\
                .touch("/tmp/mytestdir/b")\
                .run()
            
            response = sultan.ls("-1 /tmp/mytestdir/").run()
            self.assertEqual( response, ['a', 'b', 'foobar'])
        finally:
            if os.path.exists('/tmp/mytestdir'):
                shutil.rmtree('/tmp/mytestdir')

    @mock.patch('sultan.api.subprocess')
    def test_run_halt_on_nonzero(self, m_subprocess):

        m_subprocess.check_output.side_effect = subprocess.CalledProcessError(1, "foobar")
        s = Sultan()
        with self.assertRaises(subprocess.CalledProcessError):
            s.foobar("-qux").run()
        
        try:
            s.foobar("-qux").run(halt_on_nonzero=False)
        except Exception, e:
            self.fail("s.foobar('-qux').run(halt_on_nonzero=False) should not raise any errors.")


    def test_basic_command_chains(self):

        sultan = Sultan()
        self.assertEqual(str(sultan.touch("/tmp/foo").ls("-1 /tmp/foo").whoami()), "touch /tmp/foo; ls -1 /tmp/foo; whoami;")

    def test_command_generation(self):

        sultan = Sultan()
        self.assertEqual(str(sultan.yum("install", "gcc")), "yum install gcc;")

        sultan = Sultan()
        self.assertEqual(str(sultan.yum("install", "-y", "gcc")), "yum install -y gcc;")

        sultan = Sultan()
        self.assertEqual(str(sultan.yum("install -y gcc")), "yum install -y gcc;")


    def test_command_generation_for_chains(self):

        sultan = Sultan()
        self.assertEqual(str(sultan.touch("/tmp/foo").and_().touch("/tmp/bar")), "touch /tmp/foo && touch /tmp/bar;")

        sultan = Sultan()
        self.assertEqual(
            str(sultan.yum("install -y gcc").and_().ls("-lah /tmp").and_().find("/ -name gcc")),
            "yum install -y gcc && ls -lah /tmp && find / -name gcc;"
        )

    def test_execution(self):
    
        sultan = Sultan()
        sultan.touch("/tmp/foo").run()
        response = sultan.ls("-1 /tmp/foo").run()
        self.assertEqual(response, ["/tmp/foo"])

    def test_and(self):

        sultan = Sultan()
        self.assertEqual(str(sultan.touch("/tmp/foo").and_().touch("/tmp/bar")), "touch /tmp/foo && touch /tmp/bar;")

    @mock.patch('sultan.api.raw_input')
    def test_stdin(self, mock_raw_input):

        mock_raw_input.return_value = 'Hodor'
        sultan = Sultan()
        self.assertEqual(sultan.stdin('What is your name?'), 'Hodor')

    def test_calling_context(self):

        sultan = Sultan.load(cwd='/tmp', test_key='test_val')
        self.assertEqual(sultan.current_context, { 'cwd': '/tmp', 'sudo': False, 'test_key': 'test_val', 'user': getpass.getuser() })

        # cwd
        with Sultan.load(cwd='/tmp') as sultan:
            self.assertEqual(sultan.current_context, { 'cwd': '/tmp', 'sudo': False, 'user': getpass.getuser() })

        # sudo
        with Sultan.load(cwd='/tmp', sudo=True) as sultan:
            self.assertEqual(sultan.current_context, { 'cwd': '/tmp', 'sudo': True, 'user': 'root' })

        with Sultan.load(cwd='/tmp', sudo=False, user="hodor") as sultan:
            self.assertEqual(sultan.current_context, { 'cwd': '/tmp', 'sudo': False, 'user': 'hodor' })

        with Sultan.load(sudo=True) as sultan:
            self.assertEqual(sultan.current_context, { 'cwd': None, 'sudo': True, 'user': 'root' })

    def test_context_for_pwd(self):

        with Sultan.load(cwd='/tmp') as sultan:
            self.assertEqual(str(sultan.ls('-lah')), 'cd /tmp && ls -lah;')

    def test_calling_context_sudo(self):

        # no sudo
        with Sultan.load(sudo=False) as sultan:
            self.assertEqual(str(sultan.ls('-lah', '/root')), 'ls -lah /root;')

        # sudo as another user
        with Sultan.load(sudo=True, user='hodor') as sultan:
            self.assertEqual(str(sultan.ls("/home/hodor")), "sudo su - hodor -c 'ls /home/hodor;'")

        # sudo as root
        with Sultan.load(sudo=True) as sultan:
            self.assertEqual(str(sultan.ls('-lah', '/root')), "sudo su - root -c 'ls -lah /root;'")

        # sudo as another user with cwd set
        with Sultan.load(sudo=True, user='hodor', cwd='/home/hodor') as sultan:
            self.assertEqual(str(sultan.ls('-lah', '.')), "sudo su - hodor -c 'cd /home/hodor && ls -lah .;'")

    def test_calling_context_wrongly(self):

        s = Sultan()
        with self.assertRaises(InvalidContextError):
            with Sultan() as s:
                pass

    def test_clear_buffer_on_error(self):

        s = Sultan()
        try:
            s.ls("/root").run()
        except:
            self.assertEqual(len(s.commands), 0)

            

class SultanCommandTestCase(unittest.TestCase):

    def test_normal(self):

        sultan = Sultan()
        command = Command(sultan, "yum")
        self.assertEqual(str(command), "yum")

    def test_where_attribute(self):

        sultan = Sultan()
        command = Command(sultan, "df")
        self.assertEqual(str(command(where="/bin")), "/bin/df;")

class PipeTestCase(unittest.TestCase):

    def test_pipe(self):

        s = Sultan()
        r = Pipe(s, '|')
        self.assertEqual(r.command, "|")
        self.assertEqual(str(r.command), "|")

class AndTestCase(unittest.TestCase):

    def test_and(self):

        s = Sultan()
        r = And(s, '&')
        self.assertEqual(r.command, "&")
        self.assertEqual(str(r.command), "&")

class TestRedirect(unittest.TestCase):

    def test_redirect_stdout_only(self):

        s = Sultan()
        r = Redirect(s, '')
        r("/tmp/foo", stdout=True)
        self.assertEqual(r.command, "1> /tmp/foo")

    def test_redirect_stderr_only(self):

        s = Sultan()
        r = Redirect(s, '')
        r("/tmp/foo", stderr=True)
        self.assertEqual(r.command, "2> /tmp/foo")

    def test_redirect_stdout_only_with_append(self):

        s = Sultan()
        r = Redirect(s, '')
        r("/tmp/foo", stdout=True, append=True)
        self.assertEqual(r.command, "1>> /tmp/foo")

    def test_redirect_stderr_only_with_append(self):

        s = Sultan()
        r = Redirect(s, '')
        r("/tmp/foo", stderr=True, append=True)
        self.assertEqual(r.command, "2>> /tmp/foo")

    def test_redirect_stdout_and_stderr(self):

        s = Sultan()
        r = Redirect(s, '')
        r("/tmp/foo", stdout=True, stderr=True)
        self.assertEqual(r.command, "&> /tmp/foo")

    def test_redirect_stdout_and_stderr_with_append(self):

        s = Sultan()
        r = Redirect(s, '')
        r("/tmp/foo", stdout=True, stderr=True, append=True)
        self.assertEqual(r.command, "&>> /tmp/foo")
        