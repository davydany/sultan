import mock
import unittest

from sultan.result import Result

class SultanResultTestCase(unittest.TestCase):

    def setUp(self):

        self.stdout = '''
drwxr-xr-x  3 davydany  wheel     102 Sep 10 08:45 27D4E633-1477-40F6-AE3B-01AA85A6CBD9
prw-rw-rw-  1 davydany  wheel       0 Sep  7 06:52 30B00D4E-939A-404E-B2EB-23CB94489B64_IN
prw-rw-rw-  1 davydany  wheel       0 Sep  7 06:52 30B00D4E-939A-404E-B2EB-23CB94489B64_OUT
prw-rw-rw-  1 davydany  wheel       0 Sep  7 06:52 456237D8-E9A4-4F77-9E8E-D9303863B2F3_IN
prw-rw-rw-  1 davydany  wheel       0 Sep  7 06:52 456237D8-E9A4-4F77-9E8E-D9303863B2F3_OUT
prw-rw-rw-  1 davydany  wheel       0 Sep  7 06:52 47798DB1-EC09-4E72-A1B1-808629D92383_IN
prw-rw-rw-  1 davydany  wheel       0 Sep  7 06:52 47798DB1-EC09-4E72-A1B1-808629D92383_OUT
prw-rw-rw-  1 davydany  wheel       0 Sep  7 06:50 671A5D52-29E0-4747-B8CA-F035ED2B1EFB_IN
prw-rw-rw-  1 davydany  wheel       0 Sep  7 06:49 671A5D52-29E0-4747-B8CA-F035ED2B1EFB_OUT
drwxr-xr-x  3 davydany  wheel     102 Sep 10 08:45 743B6A79-82A4-471F-A9E8-B5BAF5B8E90B
drwxr-xr-x  2 davydany  wheel      68 Sep  7 06:52 814486EC-476D-47F1-AEBC-8E813E890B83
        '''

        self.stderr = '''
ls: /foobar: No such file or directory
ls: /root: No such file or directory
        '''

    @mock.patch("sultan.result.subprocess")
    def test_stdout(self, m_subprocess):
        m_subprocess.Popen = mock.Mock()
        m_subprocess.Popen().communicate.return_value = (self.stdout, self.stderr)
        result = Result(m_subprocess, [], {})
        self.assertEqual(result.stdout, self.stdout.strip().splitlines())

    @mock.patch("sultan.result.subprocess")
    def test_stderr(self, m_subprocess):
        m_subprocess.Popen = mock.Mock()
        m_subprocess.Popen().communicate.return_value = (self.stdout, self.stderr)
        result = Result(m_subprocess, [], {})
        self.assertEqual(result.stderr, self.stderr.strip().splitlines())
