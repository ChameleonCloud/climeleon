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

# Install dependencies for clouds2rc
RUN apk add --no-cache bash jq
COPY clouds2rc /usr/local/bin/

RUN mkdir /work
WORKDIR /work

COPY clouds.yaml ./

