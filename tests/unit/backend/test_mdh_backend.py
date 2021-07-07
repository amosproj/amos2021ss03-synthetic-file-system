# Python imports
import os
import unittest
import stat
from pathlib import Path
from tempfile import gettempdir

# Local imports
from sfs.backend.mdh import MDHBackend
from sfs.backend.mdh.backend_updater import MDHBackendUpdater
from sfs.dir_tree import DirectoryTree


class TestMDHBackend(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Paths
        cls.tmp_dir = gettempdir()
        cls.file_path = Path(__file__)
        cls.file_directory_path = cls.file_path.parent

        cls.file_path_symlink = Path(cls.tmp_dir) / "symlink_to_test_sfs_fuse"
        if not cls.file_path_symlink.exists():
            cls.file_path_symlink.symlink_to(cls.file_path)

        # Instantiate mdh backend without initialising it
        cls.backend = MDHBackend.__new__(MDHBackend)

        cls.backend.file_path_cache = set()
        cls.backend.name = "mdh"
        cls.backend.result_structure = "mirror"
        cls.backend.directory_tree = DirectoryTree()
        cls.backend.backend_updater = MDHBackendUpdater.__new__(MDHBackendUpdater)
        cls.backend.backend_updater.cache_path = Path(cls.tmp_dir) / "cache.txt"

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

    def test_getattr_with_partner_directory_returns_valid_stat(self) -> None:
        directory_stat = self.backend.getattr("/" + self.backend.name)
        self.assertEqual(directory_stat["st_mode"], stat.S_IFDIR | 0o755, "Test if directory has the right mode")

    def test_getattr_with_existing_directory_returns_valid_stat(self) -> None:
        actual_directory_stat = self.file_directory_path.stat()
        directory_stat = self.backend.getattr("/" + self.backend.name + str(self.file_directory_path))

        self.assertEqual(directory_stat["st_size"], actual_directory_stat.st_size, "Test if directory size is equal")
        self.assertEqual(directory_stat["st_mode"], stat.S_IFDIR | 0o755, "Test if directory has the right mode")

    # =================
    # File method tests
    # =================

    def test_utimens_with_directory_changes_times(self) -> None:
        actual_directory_stat = os.stat(self.file_directory_path)
        self.backend.utimens("/" + self.backend.name + str(self.file_directory_path))
        directory_stat = os.stat(self.file_directory_path)

        self.assertGreater(directory_stat.st_atime, actual_directory_stat.st_atime, "Test if access time changed")
        self.assertGreater(directory_stat.st_mtime, actual_directory_stat.st_mtime, "Test if modified time changed")

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
