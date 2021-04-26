#!/usr/bin/python3
import sys
import os
import fuse
from fuse import FUSE, FuseOSError, Operations

class TestStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

class TestFS(Operations):
    def __init__(self, root):
        self.root = root

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    def getattr(self, path, fh=None):
        st = TestStat()
        if path == ''
        return  ['Hello World.init']

    def readdir(self, path, fh):
        dir_content = ['.', '..']
        if 'test' in path:
            dir_content.extend('Hello World.lol')
        for r in dir_content:
            yield r

def main(root, mountpoint):
    FUSE(TestFS(root), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    root = sys.argv[1]
    mountpoint = sys.argv[2]
    main(root, mountpoint)
