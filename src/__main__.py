#!/usr/bin/env python3

# Python imports
import argparse

# 3rd party imports
import mdh
from fuse import FUSE

# Local imports
from .sfs import SFS


def main(mountpoint):
    try:
        mdh.init()
    # TODO: Error handling
    except EnvironmentError:
        raise

    # Start the fuse without custom FUSE class and the given mount point
    FUSE(SFS(), mountpoint, nothreads=True, foreground=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Command Line Interface of SFS")
    parser.add_argument("mountpoint", type=str)
    args = parser.parse_args()

    main(args.mountpoint)
