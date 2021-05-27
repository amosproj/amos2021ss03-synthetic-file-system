# Python imports
from __future__ import with_statement
import os
import stat
import time

# 3rd party imports
import pyinotify
from anytree import Node, RenderTree, Resolver
from fuse import Operations

# Local imports
from .config_notifier import ConfigFileEventHandler
from .fuse_utils import build_tree_from_files
from .mdh_bridge import MDHQueryRoot
from .paths import CONFIG_PATH, CONFIG_FILE_PATH

CORE_NAME = "core-sfs"  # FIXME: Set the name corresponding to your mdh-core


class SFS_Stat:
    """
    class that is used to represent the stat struct used by the Linux kernel, where it is used to store/access
    metadata for files. For more information on the specific variables see stat(2)
    """
    st_mode: int = stat.S_IFDIR | 0o755
    st_nlink: int = 1
    st_uid: int = 0
    st_gid: int = 0
    st_rdev: int = 0
    st_size: int = 100
    st_blksize: int = 4096
    st_blocks: int = (int)((st_size + st_blksize - 1) / st_blksize)

    st_atime: int = 0
    st_mtime: int = 0
    st_ctime: int = 0


class SFS(Operations):
    """
    Main class of the FUSE. Responsible for correctly sending the information from the MDH to the filesystem via
    the hooked function calls. For more information see https://github.com/fusepy/fusepy
    """

    def __init__(self, root=""):
        """
        Sets the directory tree up using the filters in config.graphql
        """
        self.directory_tree = Node
        self.metadatahub_files = None
        self.root = root

        query_root = MDHQueryRoot(CORE_NAME, CONFIG_FILE_PATH)
        query_root.send_request_get_result()

        self.mdh_files = query_root.result['searchMetadata']['files']
        self.directory_tree = build_tree_from_files(self.mdh_files)

        print(RenderTree(self.directory_tree))
        print("fuse running")

    def init(self, path):
        # Watch change events for config file
        self._set_up_config_notifier()

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
        print("chmod called")
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        print("chown called")
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        path_stat = SFS_Stat()
        print(f"getattr called with: {path}")

        os_path = os.stat(path)

        path_stat.st_size = os_path.st_size
        path_stat.st_blocks

        now = time.time()
        path_stat.st_atime = now
        path_stat.st_mtime = now
        path_stat.st_ctime = now

        if path in [".", "..", "/"]:
            path_stat.st_mode = stat.S_IFDIR | 0o755
            return path_stat.__dict__

        file_finder = Resolver("name")
        path = path[1:]  # strip leading "/"
        path_node: Node = file_finder.get(self.directory_tree, path)
        if len(path_node.children) == 0:
            print("got regular file")
            path_stat.st_mode = stat.S_IFREG | 0o755
        else:
            path_stat.st_mode = stat.S_IFDIR | 0o755
        return path_stat.__dict__

    def readdir(self, path, fh):

        print(f"readdir called with {path}")
        children = [".", ".."]

        file_finder = Resolver("name")
        path = path[1:]  # strip leading "/"
        path_node: Node = file_finder.get(self.directory_tree, path)

        child: Node
        for child in path_node.children:
            children.append(child.name)
            print(f"added {child.name}")
        return children

    def readlink(self, path):
        print("readlink called")
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        print("mknod called")
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        print("rmdir called")
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        print("mkdir called")
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        print("statfs called")
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
                                                         'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files',
                                                         'f_flag',
                                                         'f_frsize', 'f_namemax'))

    def unlink(self, path):
        print("unlink called")
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        print("symlink called")
        return os.symlink(target, self._full_path(name))

    def rename(self, old, new):
        print("rename called")
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        print("link called")
        return os.link(self._full_path(name), self._full_path(target))

    def utimens(self, path, times=None):
        print("utimens called")
        return os.utime(self._full_path(path), times)

    # ============
    # File methods
    # ============

    def open(self, path, flags):
        print("open called with path " + path)
        # full_path = self._full_path(path)
        return os.open(path, flags)

    def create(self, path, mode, fi=None):
        print("create called")
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        print("read called")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        print("write called")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        print("truncate called")
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        print("flush called")
        return os.fsync(fh)

    def release(self, path, fh):
        print("release called")
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        print("fsync called")
        return self.flush(path, fh)
