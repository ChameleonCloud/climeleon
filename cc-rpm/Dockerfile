FROM centos:7

RUN yum install -y git-core rpm-build spectool \
  && yum clean all

VOLUME ["/work"]
WORKDIR /work

COPY bin/ /usr/local/bin/

