# Python imports
import logging
import os
from errno import EACCES

# Local imports
from fuse import FuseOSError
from pathlib import Path
from sfs.backend import Backend


class PassthroughBackend(Backend):

    """
    Example Backend that just passes all requests to the OS
    """
    def __init__(self, id: int, instance_cfg):
        """
        Constructor
        :param instance_cfg: the config contains everything that the Passthrough backend needs.
        Currently this is only the path to the target directory.
        """
        self.id = id
        self.name = f'passthrough{id}'
        self.result_structure = instance_cfg.get("resultStructure")
        self.target_dir = instance_cfg['path']
        self.root = self.target_dir
        self.file_paths = []
        self._update_paths()

    def _update_paths(self):
        self.file_paths = [f'/{self.name}']
        prefix = len(str(Path(self.target_dir)))
        self.file_paths += [f'/{self.name}{str(p)[prefix:]}' for p in Path(self.target_dir).glob('**/*')]
        print(self.file_paths)

    def get_file_paths(self):
        return self.file_paths

    def contains_path(self, path: str) -> bool:
        """
        Checks if a certain path is held by the backend
        :param path: string representing the path that is investigated
        :return: true if the path is held by the backend, false otherwise
        """
        return path in self.file_paths

    def _full_path(self, partial):
        if partial.startswith(f'/{self.name}'):
            partial = partial[len(self.name)+2:]
        elif partial.startswith('/'):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        logging.info("access called")
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(EACCES)
        return 0

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
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in (
            'st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime',
            'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        logging.info("readdir called")

        full_path = self._full_path(path)
        return ['.', '..'] + os.listdir(full_path)

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
        full_path = self._full_path(path)
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

    def getxattr(self, path, name, position=0):
        print("getxattr called")
        return os.getxattr(self._full_path(path), name)

    def listxattr(self, path):
        logging.info("listxattr called")
        return os.listxattr(self._full_path(path))

    def setxattr(self, path, name, value, options, position=0):
        logging.info("setxattr called")
        return os.setxattr(self._full_path(path), name, value, options)

    def removexattr(self, path, name):
        logging.info("removexattr called")
        return os.removexattr(self._full_path(path), name)
