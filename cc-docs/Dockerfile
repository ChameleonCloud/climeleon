FROM alpine:3.7

RUN apk add --no-cache bash curl jq

RUN mkdir /work
WORKDIR /work

COPY bin /work/bin
ENV PATH="/work/bin:${PATH}"
ENV TERM="xterm-256color"
