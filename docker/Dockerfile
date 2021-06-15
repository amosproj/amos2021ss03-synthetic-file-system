# syntax=docker/dockerfile:1
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN groupadd --gid 1000 sfs \
  && useradd --uid 1000 --gid sfs --shell /bin/bash sfs

RUN mkdir /home/sfs
RUN chown sfs:sfs /home/sfs

RUN apt-get update && apt-get install -y \
    xauth \
    nautilus \
    libfuse-dev \
    python3-pip \
    zsh \
    wget \
    curl \
    tmux \
    vim \
    nano \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
COPY mount.sh mount.sh
<<<<<<< HEAD
<<<<<<< HEAD
COPY ./sfs/ ./sfs/
=======
COPY ./src/ ./src/
>>>>>>> 1255e9d9bd8f3cbf5195f0e00c0b560478181596
=======
COPY ./src/ ./src/
>>>>>>> 1255e9d9bd8f3cbf5195f0e00c0b560478181596
COPY ./config/ ./config/

ENV MDH_HOME=/app/mdh/

RUN pip3 install -r requirements.txt

COPY mdh-1.5.0-py3-none-any.whl mdh-1.5.0-py3-none-any.whl
RUN pip3 install mdh-1.5.0-py3-none-any.whl

RUN mkdir -p /fuse_mount

CMD ["bash"]
