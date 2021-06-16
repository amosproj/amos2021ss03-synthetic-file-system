#!/bin/bash
HOST=$1
USERNAME=$2
shift  # drop the HOST
shift  # drop the USERNAME
PASSWORD=$@  # PASSWORD is whatever remains
if [[ $1 == "run" ]]

cd src
python3 main.py ~/fuse_mount
python3 config_parser.py ~/fuse_mount
python3 fuse_utils.py ~/fuse_mount
python3 mdh_bridge.py ~/fuse_mount
python3 test_mdh.py ~/fuse_mount
cd /fuse_mount