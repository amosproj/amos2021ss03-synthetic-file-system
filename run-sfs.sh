#!/usr/bin/bash

if [[ <get first argument> == "pytest" ]]; then
    shift 1  # if you start the script with ./run-sfs.sh pytest -v, pytest will be shiftet away so "$1" is now "-v"
    <insert command for pytest>
elif [[ <insert condition for flake8> ]]; then
    <insert command for flake8>
else
    python3 "-m" "sfs" "$@"  # "$@" corresponds to all the arguments that were not shifted away
fi