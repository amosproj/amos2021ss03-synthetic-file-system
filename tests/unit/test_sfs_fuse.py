# Python imports
import os
import unittest
import stat
from mimetypes import guess_type
from pathlib import Path
from string import ascii_uppercase
from random import choice

# 3rd party imports
from fuse import FuseOSError

# Local imports
from src.fuse_utils import build_tree_from_files
from src.sfs import SFS


class TestSFSFuse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # paths
        random_string = ''.join(choice(ascii_uppercase) for i in range(42))
        cls.dummy_path = f"/tmp/{random_string}"
        cls.file_path = Path(__file__)
        cls.file_directory = cls.file_path.parent

        # instantiate sfs without initialising it
        cls.sfs = SFS.__new__(SFS)

        # build directory tree
        stat = cls.file_path.stat()
        cls.sfs.directory_tree = build_tree_from_files([{'id': '1', 'metadata': [
                {'name': 'FileName', 'value': f'{__name__}'},
                {'name': 'FileSize', 'value': f'{stat.st_size}'},
                {'name': 'MIMEType', 'value': f'{guess_type(__file__)}'},
                {'name': 'FileInodeChangeDate', 'value': f'{stat.st_ctime}'},
                {'name': 'SourceFile', 'value': f'{__file__}'},
        ]}])

    # =======================
    # Test Filesystem methods
    # =======================

    def test_access_returns_0(self) -> None:
        access_r_ok = self.sfs.access(str(self.file_path), os.R_OK)
        self.assertEqual(access_r_ok, 0, "Test whether the file exists and grants read access")

    def test_access_raises_fuse_os_error(self) -> None:
        self.assertRaises(FuseOSError, self.sfs.access, str(self.dummy_path), os.R_OK)

    def test_gettattr_with_file_returns_valid_stat(self) -> None:
        actual_file_stat = self.file_path.stat()
        valid_file_stat = self.sfs.getattr(str(self.file_path))
        self.assertEqual(valid_file_stat['st_size'], actual_file_stat.st_size)
        self.assertEqual(valid_file_stat['st_mode'], stat.S_IFREG | 0o755)  # mode probably might change

    def test_gettattr_with_directory_returns_valid_stat(self) -> None:
        actual_directory_stat = self.file_directory.stat()
        valid_directory_stat = self.sfs.getattr(str(self.file_directory))
        self.assertEqual(valid_directory_stat['st_size'], actual_directory_stat.st_size)
        self.assertEqual(valid_directory_stat['st_mode'], stat.S_IFDIR | 0o755)  # mode probably might change

    def test_readdir(self) -> None:
        self.assertTrue(True)

    def test_readlink(self) -> None:
        self.assertTrue(True)

    def test_statfs(self) -> None:
        self.assertTrue(True)

    # =================
    # Test File methods
    # =================

    def test_read(self) -> None:
        self.assertTrue(True)
