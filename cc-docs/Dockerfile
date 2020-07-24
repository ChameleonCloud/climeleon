FROM centos:8

RUN dnf install -y bash curl jq

RUN mkdir /work
WORKDIR /work

COPY bin /work/bin
ENV PATH="/work/bin:${PATH}"
ENV TERM="xterm-256color"
