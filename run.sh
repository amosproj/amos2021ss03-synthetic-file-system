#!/bin/bash

docker run \
    -p 8080:8080 \
    -v /home/data:/filesystem  \
    -v metadatahub-database:/var/lib/postgresql/12/main \
    amosproject2/metadatahub &>/dev/null & disown;

docker run -it --net="host" --cap-add=SYS_ADMIN  --device=/dev/fuse --security-opt apparmor:unconfined --tty fuse_skeleton