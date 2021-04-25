# syntax=docker/dockerfile:1
FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    libfuse-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

#COPY requirements.txt requirements.txt

#RUN pip3 install -r requirements.txt