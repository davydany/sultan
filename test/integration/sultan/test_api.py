import os
import shutil
import stat
import tempfile
import unittest
from sultan.api import Sultan

class SultanCreateFileTestCase(unittest.TestCase):
    """
    Creates a test script, ensures that the contents are valid and attempts to 
    run it, and check that it is valid.
    """

    def setUp(self):

        self.f, self.path = tempfile.mkstemp()

    def test_create_script(self):
        
        s = Sultan()
        s.clear()
        self.assertEqual(
            str(s.echo("'ls -lah /tmp'").redirect(self.path, stdout=True)),
            "echo 'ls -lah /tmp' 1> %s;" % self.path)

        s.run()
        with open(self.path) as f:
            self.assertEqual(f.read(), 'ls -lah /tmp\n')

class SultanEnvironment(unittest.TestCase):
    """
    Tests if Sultan can set environment variables.
    """

    def test_environment_setup(self):

        with Sultan.load(env={ 'FOOBAR': '/tmp' }) as s:

            response = s.env().run()
            self.assertIn('FOOBAR=/tmp', response.stdout)


class SultanExecutable(unittest.TestCase):
    """
    Tests for the executable being used
    """

    def test_default_executable(self):

        with Sultan.load() as sultan:
            result = sultan.ps().pipe().grep('`echo $$`').pipe().awk("'{ print $4 }'").run()
            self.assertEqual(result.stdout[0], '/bin/sh')

    def test_custom_executable(self):

        with Sultan.load(executable='/bin/bash') as sultan:
            result = sultan.ps().pipe().grep('`echo $$`').pipe().awk("'{ print $4 }'").run()
            self.assertEqual(result.stdout[0], '/bin/bash')

    def test_nonexistent_executable(self):
        with self.assertRaises(IOError):
            with Sultan.load(executable='no_such_exe_cause_sultan') as sultan:
                sultan.ls().run()


class SultanRunCustomScripts(unittest.TestCase):
    """
    Run a custom script that we create
    """

    def setUp(self):

        content = """
#!/usr/bin/env bash

OUTPUT_FILENAME=/tmp/SultanRunScript/lorum.txt
mkdir -p /tmp/SultanRunScript
echo 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n' > $OUTPUT_FILENAME 
echo 'Nunc in enim dictum, consectetur ex vehicula, fermentum orci.\n' > $OUTPUT_FILENAME
echo 'Donec sapien turpis, mattis vel urna sed, iaculis aliquam purus.\n' > $OUTPUT_FILENAME 
        """
        self.dir_path = '/tmp/SultanRunScript'
        self.script_filepath = '/tmp/SultanRunScript/myscript'
        self.output_filepath = '/tmp/SultanRunScript/lorum.txt'
        if os.path.exists(self.dir_path): shutil.rmtree(self.dir_path)

        s = Sultan()
        os.mkdir(self.dir_path)
        with open(self.script_filepath, 'w') as f:
            f.write(content)
        st = os.stat(self.script_filepath)
        os.chmod(self.script_filepath, st.st_mode | stat.S_IEXEC)


    def test_run_custom_script(self):
        try:
            s = Sultan()
            response = s.myscript(where=self.dir_path).run()
            self.assertEqual(len(response.stdout), 0)

            response = s.cat(self.output_filepath).run()
            self.assertEqual(response.stdout, ['Donec sapien turpis, mattis vel urna sed, iaculis aliquam purus.'])
        finally:
            shutil.rmtree(self.dir_path)


class SultanReturnCode(unittest.TestCase):
    """
    Checks on the rc (return code).
    """

    def test_zero_rc(self):
        with Sultan.load() as s:
            response = s.ls().run()
            self.assertEqual(response.rc, 0)

    def test_non_zero_rc(self):
        with Sultan.load() as s:
            response = s.exit(22).run()
            self.assertEqual(response.rc, 22)
