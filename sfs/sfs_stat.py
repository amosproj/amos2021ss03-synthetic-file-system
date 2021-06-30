import stat


class SFSStat:
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
    st_blocks: int = int((st_size + st_blksize - 1) / st_blksize)

    st_atime: int = 0
    st_mtime: int = 0
    st_ctime: int = 0
