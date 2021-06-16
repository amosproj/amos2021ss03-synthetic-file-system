"""Command Line interface of the SFS."""

# Python imports
import argparse

# 3rd party imports
from fuse import FUSE

# Local imports
from .sfs import SFS


def main() -> None:
    """Run CLI."""
    parser = argparse.ArgumentParser(
        prog='sfs',
        description="Command Line Interface of SFS"
    )
    parser.add_argument("--mountpoint", type=str)
    args = parser.parse_args()

    sfs = SFS(args.mountpoint)
    FUSE(sfs, sfs.mountpoint, nothreads=True, foreground=True)
