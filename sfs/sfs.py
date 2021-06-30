# Python imports
from __future__ import with_statement

import errno
import os
import stat
import time
from errno import EACCES

# 3rd party imports
import anytree.resolver
import fuse
from fuse import Operations, FuseOSError
import logging
import mdh
import pyinotify
from fuse import FUSE, Operations

# Local imports
from sfs.config import ConfigFileEventHandler
from sfs.config import SFSConfig
from sfs.backend import BackendManager
from .dir_tree import DirectoryTree
from .sfs_stat import SFSStat
from .paths import CONFIG_PATH

CORE_NAME = "core-test"  # FIXME: Set the name corresponding to your mdh-core


class SFS(Operations):
    """
    Main class of the FUSE. Responsible for correctly sending the information from the MDH to the filesystem via
    the hooked function calls. For more information see https://github.com/fusepy/fusepy
    """

    def __init__(self, mountpoint=None):
        self.sfs_config = SFSConfig()
        self.sfs_config.init()
        self.mountpoint = mountpoint
        if self.mountpoint is None:
            self.mountpoint = self.sfs_config.mountpoint

        self.directory_tree = DirectoryTree(algorithm=self.sfs_config.tree_algorithm)
        self.directory_tree.build(BackendManager().get_file_paths())
        self.directory_tree.print_tree()

    def init(self, path):
        # Watch change events for config file
        # self._set_up_config_notifier()
        pass

    def _set_up_config_notifier(self):
        """
        Create the event handler and run the watch in a seperate thread so that it doesn't block our main thread
        """
        event_handler = ConfigFileEventHandler(self, CORE_NAME)
        watch_manager = pyinotify.WatchManager()

        notifier = pyinotify.ThreadedNotifier(watch_manager, event_handler)
        notifier.start()

        watch_manager.add_watch(CONFIG_PATH, pyinotify.IN_MODIFY)

    # =======
    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # ==================
    # Filesystem methods
    # ==================

    def access(self, path, mode):
        print("access called")
        # full_path = self._full_path(path)
        # if not os.access(full_path, mode):
        #    raise FuseOSError(errno.EACCES)
        return 0

    def chmod(self, path, mode):
        return BackendManager().get_backend_for_path(path).chmod(path, mode)

    def chown(self, path, uid, gid):
        return BackendManager().get_backend_for_path(path).chown(path, uid, gid)

    def getattr(self, path, fh=None):
        print(f"getattr called with path {path}")
        path_stat = SFSStat()
        now = time.time()
        path_stat.st_atime = now
        path_stat.st_mtime = now
        path_stat.st_ctime = now


        if path in [".", "..", "/"]:
            path_stat.st_mode = stat.S_IFDIR | 0o755
            return path_stat.__dict__

        backend_manager = BackendManager().get_backend_for_path(path)
        if not backend_manager:
            parent_path = path.rsplit("/", 1)[0]
            backend_manager = BackendManager().get_backend_for_path(parent_path)
            if not backend_manager:
                logging.error(f"Invalid path for getattr with path {path}!")
                return path_stat.__dict__
        return backend_manager.getattr(path, fh)

    def readdir(self, path, fh):
        logging.info(f"Readdir called with path {path}")
        if 'Passthrough' in path:
            return BackendManager().get_backend_for_path(path).readdir(path, fh)
        # children = self.directory_tree.get_children(path)
        return BackendManager().get_backend_for_path(path).readdir(path, fh)
        # return children

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
        logging.error(f"create in sfs called! with path {path}")
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
