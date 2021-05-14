#!/usr/bin/python3
# ----
# The starting point is the FUSE implementation from
# https://github.com/skorokithakis/python-fuse-sample/blob/master/passthrough.py
# ---

from __future__ import with_statement

import os
import sys
# import errno
import stat
# import anytree

from fuse import FUSE, Operations  # FuseOSError
from mdh_bridge import MDHQueryRoot, MDHQuery_searchMetadata, MDHFile, MDHMetadatum, MDHResultSet
from anytree import Node, RenderTree, Resolver
import fuse_utils
import config_parser


class FuseStat:
    st_atime: int = 0
    st_ctime: int = 0
    st_gid: int = 0
    st_mode: int = stat.S_IFDIR | 0o755
    st_mtime: int = 0
    st_nlink: int = 1
    st_size: int = 43000


class MDH_FUSE(Operations):
    metadatahub_files = None  # type: [MDHFile]

    directory_tree = Node

    def __init__(self, root):
        self.root = root

        # Set up our files
        query_root = MDHQueryRoot()
        query = config_parser.create_query_from_config("../config.cfg")
        query.result.files = MDHFile()
        query.result.files.metadata = MDHMetadatum()
        query.result.files.metadata.value = True
        query.result.files.metadata.name = True
        query_root.queries.append(query)

        query_root.build_and_send_request()  # type: MDHResultSet
        self.metadatahub_files = query_root.queries[0].result.files
        self.directory_tree = fuse_utils.build_tree_from_files(self.metadatahub_files)
        print(RenderTree(self.directory_tree))
        print("fuse running")

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

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

        path_stat = FuseStat()
        print(f"getattr called with: {path}")

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
        # full_path = self._full_path(path)

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

    # File methods
    # ============

    def open(self, path, flags):
        print("open called with path " + path)
        full_path = path
        return os.open(full_path, flags)

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


def main(mountpoint, root):
    FUSE(MDH_FUSE(root), mountpoint, nothreads=True, foreground=True, **{'allow_other': True})


if __name__ == '__main__':
    # Hello from Dominik
    # Hello from Marlon
    # Hello from Vaidehi
    # Hello from Matti <3
    # Hello from Charinee <3
    # Hello from Sandra
    main(sys.argv[2], sys.argv[1])
