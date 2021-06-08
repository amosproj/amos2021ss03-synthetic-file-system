"""Command Line interface of the SFS."""

# Python imports
import argparse

# 3rd party imports
import mdh
from fuse import FUSE

# Local imports
from .sfs import SFS


def main() -> None:
    """Run CLI."""
    parser = argparse.ArgumentParser(
        prog='sfs',
        description="Command Line Interface of SFS"
    )
    parser.add_argument("mountpoint", type=str)
    args = parser.parse_args()

    # Start the fuse without custom FUSE class and the given mount point
    FUSE(SFS(), args.mountpoint, nothreads=True, foreground=True)
