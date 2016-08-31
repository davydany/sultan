import os
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