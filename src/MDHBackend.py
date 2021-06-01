import Backend
from FUSEStat import SFSStat
from anytree import Node, Resolver
import logging
import os
import time
import stat


class MDHBackend(Backend.Backend):
    """
    Implementation of the Backend interface for the MDH.
    For documentation of the functions see Backend.py
    """

    def __init__(self, root: Node):
        """
        Constructor
        :param root: the root node of the directory tree of the files that the backend is holding
        """
        self.directory_root = root

    def contains_path(self, path: str) -> bool:
        file_finder = Resolver("name")
        path = path[1:]  # strip leading "/"
        path_node: Node = file_finder.get(self.directory_root, path)
        return path_node is not None

    def get_directory_tree(self) -> Node:
        return self.directory_root

    def access(self, path, mode):
        logging.info("access called!")
        return 0

    def chmod(self, path, mode):
        logging.info("chmod called!")
        raise NotImplementedError()

    def chown(self, path, uid, gid):
        logging.info("chown called!")
        raise NotImplementedError()

    def getattr(self, path, fh=None):
        logging.info("getattr called!")
        path_stat = SFSStat()
        os_path = os.stat(path)

        path_stat.st_size = os_path.st_size

        now = time.time()
        path_stat.st_atime = now
        path_stat.st_mtime = now
        path_stat.st_ctime = now

        if path in [".", "..", "/"]:
            path_stat.st_mode = stat.S_IFDIR | 0o755
            return path_stat.__dict__

        file_finder = Resolver("name")
        path = path[1:]  # strip leading "/"
        path_node: Node = file_finder.get(self.directory_root, path)
        if len(path_node.children) == 0:
            print("got regular file")
            path_stat.st_mode = stat.S_IFREG | 0o755
        else:
            path_stat.st_mode = stat.S_IFDIR | 0o755
        return path_stat.__dict__

    def readdir(self, path, fh):
        logging.info("readdir called!")

        print(f"readdir called with {path}")
        children = [".", ".."]

        file_finder = Resolver("name")
        path = path[1:]  # strip leading "/"
        path_node: Node = file_finder.get(self.directory_root, path)

        child: Node
        for child in path_node.children:
            children.append(child.name)
            print(f"added {child.name}")
        return children

    def readlink(self, path):
        logging.info("readlink called!")
        raise NotImplementedError()

    def mknod(self, path, mode, dev):
        logging.info("mknod called!")
        raise NotImplementedError()

    def rmdir(self, path):
        logging.info("rmdir called!")
        raise NotImplementedError()

    def mkdir(self, path, mode):
        logging.info("mkdir called!")
        raise NotImplementedError()

    def statfs(self, path):
        logging.info("statfs called!")
        raise NotImplementedError()

    def unlink(self, path):
        logging.info("unlink called!")
        raise NotImplementedError()

    def symlink(self, name, target):
        logging.info("symlink called!")
        raise NotImplementedError()

    def rename(self, old, new):
        logging.info("rename called!")
        raise NotImplementedError()

    def link(self, target, name):
        logging.info("link called!")
        raise NotImplementedError()

    def utimens(self, path, times=None):
        logging.info("utimens called!")
        raise NotImplementedError()

    def open(self, path, flags):
        logging.info("open called!")
        return os.open(path, flags)

    def create(self, path, mode, fi=None):
        logging.info("create called!")
        raise NotImplementedError()

    def read(self, path, length, offset, fh):
        logging.info("read called!")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        logging.info("write called!")
        raise NotImplementedError()

    def truncate(self, path, length, fh=None):
        logging.info("truncate called!")
        raise NotImplementedError()

    def flush(self, path, fh):
        logging.info("flush called!")
        raise NotImplementedError()

    def release(self, path, fh):
        logging.info("release called!")
        raise NotImplementedError()

    def fsync(self, path, fdatasync, fh):
        logging.info("fsync called!")
        raise NotImplementedError()
