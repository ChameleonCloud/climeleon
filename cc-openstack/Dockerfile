ARG PYTHON_VER=3.9
FROM python:${PYTHON_VER}-slim

ENV XDG_CACHE_HOME="/tmp/.cache/"

RUN --mount=type=cache,target=$XDG_CACHE_HOME \
  apt update && apt install -f -y \
    gcc make \
    git \
    jq

RUN --mount=type=cache,target=$XDG_CACHE_HOME \
  pip3 install poetry

# Provide a volume-mount for a current working directory (of the host)
VOLUME ["/host"]
WORKDIR /host

COPY pyproject.toml poetry.lock ./
RUN --mount=type=cache,target=$XDG_CACHE_HOME \
  poetry config virtualenvs.create false && \
  poetry install --no-interaction

COPY clouds2rc /usr/local/bin/
COPY scripts/* /usr/local/bin/
COPY clouds*.yaml /etc/openstack/
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
