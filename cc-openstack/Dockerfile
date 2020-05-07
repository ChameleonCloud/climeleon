FROM python:2-alpine3.9 as base

# Builder (helper) image
# This image is used to install pip packages, which are then simply copied
# to the runtime image. This is to avoid having to keep the build dependencies
# for the python modules that require a build step.
FROM base as builder
ARG openstack_release=rocky

RUN apk add --no-cache \
  build-base curl git linux-headers libffi-dev libxml2-dev libxslt-dev \
  openssl-dev python-dev

RUN mkdir -p /var/lib/cc/venv
RUN pip install virtualenv && virtualenv /var/lib/cc/venv

COPY requirements.txt /requirements.txt
COPY requirements.forks.txt /requirements.forks.txt
RUN curl -Sso /upper-constraints.txt "https://raw.githubusercontent.com/openstack/requirements/stable/${openstack_release}/upper-constraints.txt" \
  && source /var/lib/cc/venv/bin/activate \
  && pip install --upgrade pip \
  && pip install -r requirements.txt -c upper-constraints.txt \
  && pip install -r requirements.forks.txt

COPY python-climeleon /opt/python-climeleon
RUN source /var/lib/cc/venv/bin/activate \
  && pip install /opt/python-climeleon

# Runtime image
FROM base

COPY --from=builder /var/lib/cc/venv /var/lib/cc/venv

# Install runtime libraries needed for wheels
RUN apk add --no-cache libffi libxml2 libxslt openssl

# Provide a volume-mount for a current working directory (of the host)
VOLUME ["/host"]
WORKDIR /host

# Install dependencies for scripts
RUN apk add --no-cache bash bc coreutils curl jq util-linux

COPY clouds2rc /usr/local/bin/
COPY scripts/* /usr/local/bin/
COPY clouds*.yaml /etc/openstack/

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
