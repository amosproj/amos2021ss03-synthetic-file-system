# Python imports
from __future__ import with_statement
import os
import stat
import time
from errno import EACCES

# 3rd party imports
import pyinotify
from anytree import Node, RenderTree, Resolver
from fuse import Operations, FuseOSError

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
        return BackendManager().get_backend_for_path(path).chmod(path, mode)

    def chown(self, path, uid, gid):
        return BackendManager().get_backend_for_path(path).chown(path, uid, gid)

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

    def create(self, path, mode, fi=None):
        return BackendManager().get_backend_for_path(path).create(path, mode, fi)

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
