#!/usr/bin/bash

if [[ "$1" == "pytest" ]]; then
    shift 1  # if you start the script with ./run-sfs.sh pytest -v, pytest will be shifted away so "$1" is now "-v"
    python "-m" "pytest" "tests/unit" "--cov=sfs" "$@"
elif [[ "$1" == "flake8" ]]; then
    shift 1
    flake8 "sfs" "tests" "--count" "--show-source" "--max-line-length=127" "--per-file-ignores=__init__.py:F401" "--statistics" "$@"
else
    python "-m" "sfs" "$@"  # "$@" corresponds to all the arguments that were not shifted away
fi

