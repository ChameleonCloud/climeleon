FROM centos:8 as base

# Builder (helper) image
# This image is used to install pip packages, which are then simply copied
# to the runtime image. This is to avoid having to keep the build dependencies
# for the python modules that require a build step.
FROM base as builder
ARG openstack_release=train
RUN --mount=type=cache,target=/var/cache/dnf dnf install -y \
  gcc \
  git \
  libffi-devel \
  libxml2-devel \
  libxslt-devel \
  make \
  openssl-devel \
  openssl-devel \
  python3-devel 


# "activate" virtualenv by adding to path
ENV VIRTUAL_ENV=/var/lib/cc/venv
RUN mkdir -p /var/lib/cc && python3 -m venv "${VIRTUAL_ENV}"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Update python tools
RUN pip3 install --upgrade pip setuptools wheel

# Add requirements
COPY requirements.txt requirements.forks.txt /
RUN curl -Sso /upper-constraints.txt "https://raw.githubusercontent.com/openstack/requirements/stable/${openstack_release}/upper-constraints.txt"

RUN mkdir -p /wheels/
# Install requirements
RUN --mount=type=cache,target=/root/.cache/pip \
  pip wheel -w /wheels/ -c upper-constraints.txt -r requirements.txt && \
  pip wheel -w /wheels/ -r requirements.forks.txt

# Runtime image
FROM base

# Install runtime libraries needed for wheels
RUN --mount=type=cache,target=/var/cache/dnf dnf install -y \
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

# Provide a volume-mount for a current working directory (of the host)
VOLUME ["/host"]
WORKDIR /host

COPY --from=builder /wheels/ /wheels/

# "activate" virtualenv by adding to path
ENV VIRTUAL_ENV=/var/lib/cc/venv
RUN mkdir -p /var/lib/cc && python3 -m venv "${VIRTUAL_ENV}"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt requirements.forks.txt ./

RUN --mount=type=cache,target=/root/.cache/pip \
  pip3 install --upgrade pip setuptools wheel && \
  pip install --find-links /wheels/ \
  -r requirements.txt \
  -r requirements.forks.txt

COPY clouds2rc /usr/local/bin/
COPY scripts/* /usr/local/bin/
COPY clouds*.yaml /etc/openstack/

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
