FROM ubuntu:latest 

RUN apt-get update && apt-get install --no-install-recommends -y bash curl jq

RUN mkdir /work
WORKDIR /work

COPY bin /work/bin
ENV PATH="/work/bin:${PATH}"
ENV TERM="xterm-256color"
