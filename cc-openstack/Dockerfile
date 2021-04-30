FROM centos:8 AS base
ARG CACHE_DIR=/tmp/cache
ENV XDG_CACHE_HOME=${CACHE_DIR}
ENV DNF_CACHE=/var/cache/dnf

# Install minimal deps
RUN --mount=type=cache,target=${DNF_CACHE} dnf install -y \
  python3

# create virtualenv and add to path
ENV VIRTUAL_ENV=/var/lib/cc/venv
RUN mkdir /var/lib/cc && python3 -m venv ${VIRTUAL_ENV}
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /var/lib/cc

# Update python tools
RUN --mount=type=cache,target=${XDG_CACHE_HOME} \
  pip3 install --upgrade pip setuptools wheel && \
  pip3 install poetry

# Builder (helper) image
# This image is used to install pip packages, which are then simply copied
# to the runtime image. This is to avoid having to keep the build dependencies
# for the python modules that require a build step.
FROM base AS builder
ARG openstack_release=train
# Install Build Dependencies
RUN --mount=type=cache,target=${DNF_CACHE} dnf install -y \
  gcc \
  git \
  libffi-devel \
  libxml2-devel \
  libxslt-devel \
  make \
  openssl-devel \
  openssl-devel \
  python3-devel 

# Add requirements
COPY pyproject.toml poetry.lock ./

# Install requirements
RUN --mount=type=cache,target=${XDG_CACHE_HOME} \
  poetry install --no-dev --no-root --no-interaction

# Runtime image
FROM base AS runtime
# Provide a volume-mount for a current working directory (of the host)
VOLUME ["/host"]
WORKDIR /host

# Install runtime libraries needed for wheels
RUN --mount=type=cache,target=${DNF_CACHE} dnf install -y \
  bash \
  bc \
  curl \
  git \
  jq \
  libffi \
  libxml2 \
  libxslt \
  openssl \
  python3 \
  which

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY clouds2rc /usr/local/bin/
COPY scripts/* /usr/local/bin/
COPY clouds*.yaml /etc/openstack/

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
