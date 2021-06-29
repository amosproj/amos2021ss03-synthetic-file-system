# Python imports
from __future__ import with_statement
import stat
import time

# 3rd party imports
import logging
from fuse import Operations

# Local imports
from sfs.config import SFSConfig
from sfs.backend import BackendManager
from .sfs_stat import SFSStat


class SFS(Operations):
    """
    Main class of the FUSE. Responsible for correctly sending the information from the MDH to the filesystem via
    the hooked function calls. For more information see https://github.com/fusepy/fusepy
    """

    def __init__(self, mount_point=None):
        self.sfs_config = SFSConfig()
        self.sfs_config.init()
        self.mount_point = mount_point
        if self.mount_point is None:
            self.mount_point = self.sfs_config.mountpoint

    # ==================
    # Filesystem methods
    # ==================

    def access(self, path, mode):
        return BackendManager().get_backend_for_path(path).access(path, mode)

    def chmod(self, path, mode):
        return BackendManager().get_backend_for_path(path).chmod(path, mode)

    def chown(self, path, uid, gid):
        return BackendManager().get_backend_for_path(path).chown(path, uid, gid)

    def getattr(self, path, fh=None):
        path_stat = SFSStat()
        now = time.time()
        path_stat.st_atime = now
        path_stat.st_mtime = now
        path_stat.st_ctime = now

        if path in [".", "..", "/"]:
            path_stat.st_mode = stat.S_IFDIR | 0o755
            return path_stat.__dict__

        backend = BackendManager().get_backend_for_path(path)
        if not backend:
            parent_path = path.rsplit("/", 1)[0]
            backend = BackendManager().get_backend_for_path(parent_path)
            if not backend:
                logging.error(f"Invalid path for getattr with path {path}!")
                return path_stat.__dict__
        return backend.getattr(path, fh)

    def readdir(self, path, fh):
        if path == '/':
            children = ['.', '..']
            for backend in BackendManager().backends:
                if hasattr(backend, 'name'):
                    children.append(backend.name)
            return children
        logging.info(f"Readdir called with path {path}")
        return BackendManager().get_backend_for_path(path).readdir(path, fh)

    def readlink(self, path):
        return BackendManager().get_backend_for_path(path).readlink(path)

    def mknod(self, path, mode, dev):
        return BackendManager().get_backend_for_path(path).mknod(path, mode, dev)

    def rmdir(self, path):
        return BackendManager().get_backend_for_path(path).rmdir(path)

    def mkdir(self, path, mode):
        return BackendManager().get_backend_for_path(path).mkdir(path, mode)

    def statfs(self, path):
        return BackendManager().get_backend_for_path(path).statfs(path)

    def unlink(self, path):
        return BackendManager().get_backend_for_path(path).unlink(path)

    def symlink(self, name, target):
        # TODO
        return BackendManager().get_backend_for_path(name).symlink(name, target)

    def rename(self, old, new):
        # TODO
        return BackendManager().get_backend_for_path(old).rename(old, new)

    def link(self, target, name):
        return BackendManager().get_backend_for_path(target).link(target, name)

    def utimens(self, path, times=None):
        return BackendManager().get_backend_for_path(path).utimens(path, times)

    # ============
    # File methods
    # ============

    def open(self, path, flags):
        return BackendManager().get_backend_for_path(path).open(path, flags)

    def create(self, path: str, mode, fi=None):
        backend_manager = BackendManager().get_backend_for_path(path)
        if not backend_manager:
            parent_path = path.rsplit("/", 1)[0]
            backend_manager = BackendManager().get_backend_for_path(parent_path)
            if not backend_manager:
                logging.error("Invalid path for create!")
                return None
        return backend_manager.create(path, mode, fi)

    def read(self, path, length, offset, fh):
        return BackendManager().get_backend_for_path(path).read(path, length, offset, fh)

    def write(self, path, buf, offset, fh):
        return BackendManager().get_backend_for_path(path).write(path, buf, offset, fh)

    def truncate(self, path, length, fh=None):
        return BackendManager().get_backend_for_path(path).truncate(path, length, fh)

    def flush(self, path, fh):
        return BackendManager().get_backend_for_path(path).flush(path, fh)

    def release(self, path, fh):
        return BackendManager().get_backend_for_path(path).release(path, fh)

    def fsync(self, path, fdatasync, fh):
        return BackendManager().get_backend_for_path(path).fsync(path, fdatasync, fh)
