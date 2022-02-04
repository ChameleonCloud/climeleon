FROM ubuntu:latest as base

# Builder (helper) image
# This image is used to install pip packages, which are then simply copied
# to the runtime image. This is to avoid having to keep the build dependencies
# for the python modules that require a build step.
FROM base as builder
ARG openstack_release=train

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install --no-install-recommends -y \
    curl \
    git-core \
    libffi-dev  `#needed for cffi on arm64, rdepend for paramiko and cryptography` \
    libxml2-dev `#needed for lxml on arm64, rdepend for python-dracclient->python-chi-operator` \
    libxslt-dev `#needed for lxml on arm64, rdepend for python-dracclient->python-chi-operator` \
    libssl-dev \
    python3-dev \
    python3-venv

RUN mkdir -p /var/lib/chi
RUN python3 -m venv /var/lib/chi/venv

COPY requirements.txt /requirements.txt
COPY requirements.forks.txt /requirements.forks.txt
RUN curl -Sso /upper-constraints.txt "https://raw.githubusercontent.com/openstack/requirements/stable/${openstack_release}/upper-constraints.txt" \
  && . /var/lib/chi/venv/bin/activate \
  && pip install --upgrade pip \
  && pip install -r requirements.txt -c upper-constraints.txt \
  && pip install -r requirements.forks.txt

# Install Chameleon libraries. These are in a separate layer because
# they change way more often than the base requirements, and it's wasteful
# to invalidate the previous layer all the time, as it's expensive.
RUN . /var/lib/chi/venv/bin/activate && \
  pip install \
  "python-chi>=0.10.0,<1.0.0" \
  "python-chi-operator>=0.4.3"

# Runtime image
FROM base

# Install runtime libraries needed for wheels
RUN apt-get update && apt-get install -y \
  bash \
  bc \
  curl \
  jq \
  openssl \
  python3

# Provide a volume-mount for a current working directory (of the host)
VOLUME ["/host"]
WORKDIR /host

COPY --from=builder /var/lib/chi/venv /var/lib/chi/venv

COPY clouds2rc /usr/local/bin/
COPY scripts/* /usr/local/bin/

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
