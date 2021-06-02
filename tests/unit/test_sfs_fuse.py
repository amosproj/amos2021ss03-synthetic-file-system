# Python imports
import os
import stat
import unittest
from mimetypes import guess_type
from pathlib import Path
from random import choice
from string import ascii_uppercase

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
        cls.dummy_path = Path(f"/tmp/{random_string}")  # Create random directory that doesn't exist
        cls.file_path = Path(__file__)
        cls.file_directory_path = cls.file_path.parent

        cls.file_path_symlink = Path("/tmp/symlink_to_test_sfs_fuse")
        if not cls.file_path_symlink.exists():
            cls.file_path_symlink.symlink_to(cls.file_path)

        # instantiate sfs without initialising it
        cls.sfs = SFS.__new__(SFS)

        # build directory tree
        stat = cls.file_path.stat()
        cls.sfs.directory_tree = build_tree_from_files([{'id': '42', 'metadata': [
                {'name': 'FileName', 'value': f'{ cls.file_path.name }'},
                {'name': 'FileSize', 'value': f'{ stat.st_size }'},
                {'name': 'MIMEType', 'value': f'{ guess_type(str(cls.file_path)) }'},
                {'name': 'FileInodeChangeDate', 'value': f'{ stat.st_ctime }'},
                {'name': 'SourceFile', 'value': f'{ str(cls.file_path) }'},
        ]}])
        cls.sfs.root = ""

    @classmethod
    def tearDownClass(cls):
        cls.file_path_symlink.unlink()

    # =======================
    # Filesystem method tests
    # =======================

    def test_access_with_existing_file_returns_0(self) -> None:
        access_r_ok = self.sfs.access(str(self.file_path), os.R_OK)
        self.assertEqual(access_r_ok, 0, "Test whether the file exists and grants read access")

    def test_access_wit_dummy_file_raises_fuse_os_error(self) -> None:
        self.assertRaises(FuseOSError, self.sfs.access, str(self.dummy_path), os.R_OK)

    def test_gettattr_with_existing_file_returns_valid_stat(self) -> None:
        actual_file_stat = self.file_path.stat()
        valid_file_stat = self.sfs.getattr(str(self.file_path))
        self.assertEqual(valid_file_stat['st_size'], actual_file_stat.st_size, "Test if file size is equal")
        # NOTE: mode probably might change
        self.assertEqual(valid_file_stat['st_mode'], stat.S_IFREG | 0o755, "Test if file has the right mode")

    def test_gettattr_with_existing_directory_returns_valid_stat(self) -> None:
        actual_directory_stat = self.file_directory_path.stat()
        valid_directory_stat = self.sfs.getattr(str(self.file_directory_path))
        self.assertEqual(valid_directory_stat['st_size'], actual_directory_stat.st_size, "Test if directory size is equal")
        # NOTE: mode probably might change
        self.assertEqual(valid_directory_stat['st_mode'], stat.S_IFDIR | 0o755, "Test if directory has the right mode")

    def test_readdir_with_existing_directory_returns_directories(self) -> None:
        readdir_directories = self.sfs.readdir(str(self.file_directory_path), None)
        self.assertEqual(len(readdir_directories), 3, "Tree should contain '.', '..' and itself")
        self.assertIn(self.file_path.name, readdir_directories, "Tree should contain the file name")

    def test_readlink_with_existing_symlink_returns_relative_path(self) -> None:
        actual_file_path = os.path.relpath(self.file_path, self.sfs.root)
        resolved_file_path = self.sfs.readlink(str(self.file_path_symlink))
        self.assertEqual(actual_file_path, resolved_file_path, "Test if relative paths are equal")

    # =================
    # File method tests
    # =================

    def test_read_with_file_returns_bytes(self) -> None:
        fh = os.open(self.file_path, os.O_RDONLY)
        file_bytes = self.sfs.read(str(self.file_path), 42, 0, fh)
        self.assertEqual(len(file_bytes), 42, "Test if number of bytes matches")
