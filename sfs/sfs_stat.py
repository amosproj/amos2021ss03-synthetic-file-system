import stat


class SFSStat:
    """
    This class is used to represent the stat struct used by the Linux kernel, where it is used to store/access
    metadata for files. For more information on the specific variables see stat(2)
    """
    def __init__(self):
        self.st_mode: int = stat.S_IFDIR | 0o755
        self.st_nlink: int = 1
        self.st_uid: int = 0
        self.st_gid: int = 0
        self.st_rdev: int = 0
        self.st_size: int = 100
        self.st_blksize: int = 4096
        self.st_blocks: int = int((self.st_size + self.st_blksize - 1) / self.st_blksize)

        self.st_atime: int = 0
        self.st_mtime: int = 0
        self.st_ctime: int = 0


class SFSStatFS:
    """
    This class is used to represent the statfs struct used by the Linux kernel, where it is used to store/access
    metadata for mounted files system. For more information on the specific variables see statfs(2)
    """
    def __init__(self):
        self.f_bsize: int = 4096         # Optimal transfer block size
        self.f_frsize: int = 4096        # Fragment size (since Linux 2.6)
        self.f_blocks: int = 42000000    # Total blocks in filesystem
        self.f_bfree: int = 42000000     # Free blocks in filesystem
        self.f_bavail: int = 42000000    # Free blocks available to unprivileged user
        self.f_files: int = 42000000     # Total inodes in filesystem
        self.f_ffree: int = 42000000     # Free inodes in filesystem
        self.f_favail: int = 42000000    # Not mentioned in statfs(2)
        self.f_flag: int = 4096          # Mount flags of filesystem
        self.f_namemax: int = 255        # Maximum length of filenames
