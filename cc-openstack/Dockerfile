FROM python:2-alpine3.7 as base

FROM base as builder

RUN apk add --no-cache build-base curl git linux-headers libffi-dev openssl-dev python-dev

RUN mkdir /install
COPY requirements.txt /requirements.txt
COPY requirements.forks.txt /requirements.forks.txt
RUN curl -Sso /upper-constraints.txt https://raw.githubusercontent.com/openstack/requirements/stable/rocky/upper-constraints.txt \
  && pip install --install-option="--prefix=/install" --no-build-isolation \
    -r requirements.txt -c upper-constraints.txt \
  && pip install --install-option="--prefix=/install" --no-build-isolation \
    -r requirements.forks.txt

FROM base

COPY --from=builder /install /usr/local

# Install runtime libraries needed for crypto
RUN apk add --no-cache libffi openssl

RUN mkdir /work
WORKDIR /work
# Provide a volume-mount for a current working directory (of the host)
VOLUME ["/mnt/cwd"]

# Install dependencies for scripts
RUN apk add --no-cache bash coreutils curl jq

COPY clouds2rc /usr/local/bin/
COPY scripts ./scripts
COPY clouds*.yaml ./

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
