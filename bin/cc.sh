#!/usr/bin/env bash
set -e -u -o pipefail

cloud="${1:-}"
shift
CHAMELEON_USER="shermanm@uchicago.edu"
password="$(getpw.sh)"
image="docker.chameleoncloud.org/cc-openstack:latest"


docker_options=(--rm --interactive --tty)
docker_options+=(-e "OS_USERNAME=$CHAMELEON_USER")
docker_options+=(-e "OS_PASSWORD=$password")
docker_options+=(-e "OS_CLOUD=$cloud")
docker_options+=(-v "$PWD:/host")
if [[ -z "${1:-}" ]]; then
  cmd="bash"
fi

exec docker run "${docker_options[@]}" "${image}" "${cmd:-$@}"
