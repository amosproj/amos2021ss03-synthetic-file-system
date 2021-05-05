# syntax=docker/dockerfile:1
FROM ubuntu:20.04

RUN groupadd --gid 1000 sfs \
  && useradd --uid 1000 --gid sfs --shell /bin/bash sfs

RUN mkdir /home/sfs
RUN chown sfs:sfs /home/sfs

RUN apt-get update && apt-get install -y \
    libfuse-dev \
    python3-pip \
    zsh \
    wget \
    curl \
    tmux \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
COPY mount.sh mount.sh
COPY ./src/ ./src/

RUN pip3 install -r requirements.txt
RUN mkdir -p /fuse_mount
RUN mkdir -p /test_root

RUN mkdir /test_root/test_sub_folder
RUN touch /test_root/test.txt /test_root/test2.text /test_root/test_sub_folder/test2.txt

RUN echo "test text" >> /test_root/test.txt
RUN echo "test2 text" >> /test_root/test_sub_folder/test2.txt

# USER sfs
#["python3"]
CMD ["bash"]
#CMD ["main.py", "/test_root", "/fuse_mount"]
