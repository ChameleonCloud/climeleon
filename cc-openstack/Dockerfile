FROM python:2-alpine3.7 as base

FROM base as builder

RUN apk add --no-cache build-base linux-headers libffi-dev openssl-dev python-dev

RUN mkdir /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r requirements.txt

FROM base

COPY --from=builder /install /usr/local

# Install runtime libraries needed for crypto 
RUN apk add --no-cache libffi openssl

RUN mkdir /work
WORKDIR /work

# Install dependencies for scripts
RUN apk add --no-cache coreutils bash jq

COPY clouds2rc /usr/local/bin/
COPY scripts ./
COPY clouds.yaml ./

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

