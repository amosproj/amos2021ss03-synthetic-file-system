import Backend
import os
from errno import EACCES
import logging
from fuse import FuseOSError
from anytree import Node, Resolver


class PassthroughBackend(Backend.Backend):

    """
    Example Backend that just passes all requests to the OS
    """
    def __init__(self, root: Node):
        """
        Constructor
        :param root: the root node of the directory tree of the files that the backend is holding
        """
        self.directory_root = root

    def get_directory_tree(self) -> Node:
        """
        Getter for the directory tree of the files that this backend is holding
        :return: the root node of the dirctory tree
        """
        return self.directory_root

    def contains_path(self, path: str) -> bool:
        """
        Checks if a certain path is held by the backend
        :param path: string representing the path that is investigated
        :return: true if the path is held by the backend, false otherwise
        """
        file_finder = Resolver("name")
        path = path[1:]  # strip leading "/"
        path_node: Node = file_finder.get(self.directory_root, path)
        return path_node is not None

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        logging.info("access called")
        if not os.access(path, mode):
            raise FuseOSError(EACCES)

    def chmod(self, path, mode):
        logging.info("chmod called")
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        logging.info("chown called")
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        logging.info("getattr called")
        st = os.lstat(path)
        return dict((key, getattr(st, key)) for key in (
            'st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime',
            'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        logging.info("readdir called")
        return ['.', '..'] + os.listdir(path)

    def readlink(self, path):
        logging.info("readlink called")
        return os.readlink(path)

    def mknod(self, path, mode, dev):
        logging.info("mknod called")
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        logging.info("rmdir called")
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        logging.info("mkdir called")
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        logging.info("statfs called")
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
                                                         'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files',
                                                         'f_flag',
                                                         'f_frsize', 'f_namemax'))

    def unlink(self, path):
        logging.info("unlink called")
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        logging.info("symlink called")
        return os.symlink(target, self._full_path(name))

    def rename(self, old, new):
        logging.info("rename called")
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        logging.info("link called")
        return os.link(self._full_path(name), self._full_path(target))

    def utimens(self, path, times=None):
        logging.info("utimens called")
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        logging.info("open called with path " + path)
        full_path = path
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        logging.info("create called")
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        logging.info("read called")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        logging.info("write called")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        logging.info("truncate called")
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        logging.info("flush called")
        return os.fsync(fh)

    def release(self, path, fh):
        logging.info("release called")
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        logging.info("fsync called")
        return self.flush(path, fh)
