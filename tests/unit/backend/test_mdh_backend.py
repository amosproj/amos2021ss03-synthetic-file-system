# Python imports
import os
import unittest
from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4

# Local imports
from sfs.backend.mdh import MDHBackend
from sfs.backend.mdh.backend_updater import MDHBackendUpdater
from sfs.dir_tree import DirectoryTree


class TestMDHBackend(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Paths
        tmp_dir = gettempdir()
        cls.dummy_path = Path(tmp_dir) / f"{uuid4()}"  # Create random path that doesn't exist
        cls.file_path = Path(__file__)
        cls.file_directory_path = cls.file_path.parent

        cls.file_path_symlink = Path(tmp_dir) / "symlink_to_test_sfs_fuse"
        if not cls.file_path_symlink.exists():
            cls.file_path_symlink.symlink_to(cls.file_path)

        # Instantiate mdh backend without initialising it
        cls.backend = MDHBackend.__new__(MDHBackend)

        cls.backend.file_path_cache = set()
        cls.backend.name = "core"
        cls.backend.result_structure = "mirror"
        cls.backend.directory_tree = DirectoryTree()
        cls.backend.backend_updater = MDHBackendUpdater.__new__(MDHBackendUpdater)
        cls.backend.backend_updater.cache_path = Path(tmp_dir) / "cache.txt"

    @classmethod
    def tearDownClass(cls):
        cls.file_path_symlink.unlink()
        cls.backend.backend_updater.cache_path.unlink()

    # =======================
    # Filesystem method tests
    # =======================

    def test_access_with_existing_file_returns_0(self) -> None:
        access_r_ok = self.backend.access(str(self.file_path), os.R_OK)
        self.assertEqual(access_r_ok, 0, "Test whether the file exists and grants read access")

    # =================
    # File method tests
    # =================

    def test_read_with_file_returns_bytes_read(self) -> None:
        byte_to_read = 42
        offset = 0

        with open(self.file_path, mode='r') as fh:
            read_bytes = self.backend.read(
                str(self.file_path),
                byte_to_read,
                offset,
                fh.fileno())

        self.assertEqual(len(read_bytes), byte_to_read, "Test if number of bytes matches")

    def test_write_with_file_returns_written_bytes(self) -> None:
        testdata = 'testtext'
        offset = 0

        with open(self.backend.backend_updater.cache_path, mode='w') as fh:
            written_bytes = self.backend.write(
                str(self.file_directory_path),
                bytes(testdata, "utf-8"),
                offset,
                fh.fileno())

        self.assertEqual(len(testdata), written_bytes, "Test if number of bytes matches")

    # ============================
    # Test not implemented methods
    # ============================

    def test_chmod_is_not_implemented(self):
        self.assertRaises(NotImplementedError, self.backend.mkdir, 42, 42)

    def test_chown_is_not_implemented(self):
        self.assertRaises(NotImplementedError, self.backend.mknod, 42, 42, 42)

    def test_readlink_is_not_implemented(self):
        self.assertRaises(NotImplementedError, self.backend.readlink, 42)

    def test_mknod_is_not_implemented(self):
        self.assertRaises(NotImplementedError, self.backend.mknod, 42, 42, 42)

    def test_rmdir_is_not_implemented(self):
        self.assertRaises(NotImplementedError, self.backend.rmdir, 42)

    def test_mkdir_is_not_implemented(self):
        self.assertRaises(NotImplementedError, self.backend.mkdir, 42, 42)

    def test_statfs_is_not_implemented(self):
        self.assertRaises(NotImplementedError, self.backend.statfs, 42)

    def test_unlink_is_not_implemented(self):
        self.assertRaises(NotImplementedError, self.backend.unlink, 42)

    def test_symlink_is_not_implemented(self):
        self.assertRaises(NotImplementedError, self.backend.symlink, 42, 42)

    def test_rename_is_not_implemented(self):
        self.assertRaises(NotImplementedError, self.backend.rename, 42, 42)

    def test_link_is_not_implemented(self):
        self.assertRaises(NotImplementedError, self.backend.link, 42, 42)

    def test_release_is_not_implemented(self):
        self.assertRaises(NotImplementedError, self.backend.link, 42, 42)