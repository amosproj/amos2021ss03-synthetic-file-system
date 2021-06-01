import abc


class Backend:

    @abc.abstractmethod
    def get_directory_tree(self):
        pass

    @abc.abstractmethod
    def get_attribute(self, path: str):
        pass

    @abc.abstractmethod
    def read_directory(self, path: str):
        pass

    @abc.abstractmethod
    def access(self, path, mode):
        pass

    @abc.abstractmethod
    def chmod(self, path, mode):
        pass

    @abc.abstractmethod
    def chown(self, path, uid, gid):
        pass

    @abc.abstractmethod
    def getattr(self, path, fh=None):
        pass

    @abc.abstractmethod
    def readdir(self, path, fh):
        pass

    @abc.abstractmethod
    def readlink(self, path):
        pass

    @abc.abstractmethod
    def mknod(self, path, mode, dev):
        pass

    @abc.abstractmethod
    def rmdir(self, path):
        pass

    @abc.abstractmethod
    def mkdir(self, path, mode):
        pass

    @abc.abstractmethod
    def statfs(self, path):
        pass

    @abc.abstractmethod
    def unlink(self, path):
        pass

    @abc.abstractmethod
    def symlink(self, name, target):
        pass

    @abc.abstractmethod
    def rename(self, old, new):
        pass

    @abc.abstractmethod
    def link(self, target, name):
        pass

    @abc.abstractmethod
    def utimens(self, path, times=None):
        pass

    @abc.abstractmethod
    def open(self, path, flags):
        pass

    @abc.abstractmethod
    def create(self, path, mode, fi=None):
        pass

    @abc.abstractmethod
    def read(self, path, length, offset, fh):
        pass

    @abc.abstractmethod
    def write(self, path, buf, offset, fh):
        pass

    @abc.abstractmethod
    def truncate(self, path, length, fh=None):
        pass

    @abc.abstractmethod
    def flush(self, path, fh):
        pass

    @abc.abstractmethod
    def release(self, path, fh):
        pass

    @abc.abstractmethod
    def fsync(self, path, fdatasync, fh):
        pass

    @abc.abstractmethod
    def contains_path(self, path: str) -> bool:
        pass
