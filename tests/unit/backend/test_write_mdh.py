# Python imports
import os
import unittest
from pathlib import Path

# 3rd party imports
from sfs.backend.mdh.backend import MDHBackend
from sfs.backend.mdh import backend_updater


class TestWrite(unittest.TestCase):

    def setUp(self):
        self.file_path = Path(__file__)
        self.file_directory_path = self.file_path.parent

        self.backend = MDHBackend.__new__(MDHBackend)
        self.backend.file_path_cache = set()
        self.backend.backend_updater = backend_updater.MDHBackendUpdater(self.backend)

    def tearDown(self):
        os.remove("test123.txt")

    def test_write(self) -> None:

        testdata = 'testtext'
        fh = os.open('test123.txt', os.O_RDWR | os.O_CREAT)
        testlength = self.backend.write(str(self.file_directory_path),
                                        bytes(testdata, 'utf-8'),
                                        0,
                                        fh
                                        )
        os.close(fh)

        self.assertEqual(len(testdata), testlength)
