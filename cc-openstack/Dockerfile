FROM centos:8 as base

# Builder (helper) image
# This image is used to install pip packages, which are then simply copied
# to the runtime image. This is to avoid having to keep the build dependencies
# for the python modules that require a build step.
FROM base as builder
ARG openstack_release=rocky

RUN dnf group install -y "Development Tools" \
  && dnf install -y openssl-devel python3-devel
# RUN dnf install -y \
#   build-base curl git linux-headers libffi-dev libxml2-dev libxslt-dev \
#   openssl-dev python-dev

RUN mkdir -p /var/lib/cc
RUN python3 -m venv /var/lib/cc/venv

COPY requirements.txt /requirements.txt
COPY requirements.forks.txt /requirements.forks.txt
RUN curl -Sso /upper-constraints.txt "https://raw.githubusercontent.com/openstack/requirements/stable/${openstack_release}/upper-constraints.txt" \
  && source /var/lib/cc/venv/bin/activate \
  && pip install --upgrade pip \
  && pip install -r requirements.txt -c upper-constraints.txt \
  && pip install -r requirements.forks.txt

# Install Chameleon libraries. These are in a separate layer because
# they change way more often than the base requirements, and it's wasteful
# to invalidate the previous layer all the time, as it's expensive.
RUN source /var/lib/cc/venv/bin/activate && \
  pip install \
    "python-chi>=0.8.1,<1.0.0" \
    "python-chi-operator>=0.3.0"

# Runtime image
FROM base

# Install runtime libraries needed for wheels
RUN dnf install -y \
  bash \
  bc \
  curl \
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

COPY --from=builder /var/lib/cc/venv /var/lib/cc/venv

COPY clouds2rc /usr/local/bin/
COPY scripts/* /usr/local/bin/
COPY clouds*.yaml /etc/openstack/

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
