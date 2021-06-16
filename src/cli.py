# Python imports
import argparse

# 3rd party imports
import mdh
from fuse import FUSE

# Local imports
from .sfs import SFS


try:
    mdh.init()
# TODO: Error handling
except EnvironmentError:
    raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Command Line Interface of SFS")
    parser.add_argument("mountpoint", type=str)
    args = parser.parse_args()

    # Start the fuse without custom FUSE class and the given mount point
    FUSE(SFS(), args.mountpoint, nothreads=True, foreground=True)
