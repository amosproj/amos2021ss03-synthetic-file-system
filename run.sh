#!/bin/bash

# docker run \
#     -p 8080:8080 \
#     -v /home/data:/filesystem  \
#     -v metadatahub-database:/var/lib/postgresql/12/main \
#     amosproject2/metadatahub &>/dev/null & disown;

docker run -it --tty \
    --network=host \
    --env DISPLAY=$DISPLAY \
    --volume /tmp/.X11-unix:/tmp/.X11-unix \
    --volume $XAUTHORITY:/root/.Xauthority \
    --cap-add=SYS_ADMIN \
    --device=/dev/fuse \
    --security-opt apparmor:unconfined \
    fuse_skeleton