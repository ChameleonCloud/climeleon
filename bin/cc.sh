#!/bin/sh
set -e -u -o pipefail

registry="docker.chameleoncloud.org"

cloud="${1:-}"
[[ -n "$cloud" ]] || {
  cat <<'USAGE'
cc: CLI helper for Chameleon

Execute:
  cc CLOUD CMD: Execute CMD against the cloud configuration identified by CLOUD.
    Any OpenStack client e.g., `openstack` or `blazar` can be run in this way.
    There are also a series of custom helper scripts that summarize or perform
    actions on the testbed. Running with no CMD opens an interactive shell.

  # Open interactive shell for TACC cloud (user creds)
  cc tacc
  # List projects for TACC cloud (admin creds)
  cc tacc_admin openstack project list
  # Inspect a Keystone token on UC cloud (admin creds)
  cc uc_admin token-inspect TOKEN
USAGE
  exit 1
}
shift # Past 'cloud' positional arg

password="$(chameleon_password "$cloud")"
if [ -z "$password" ]; then
  cat <<NOPASSWD
Could not find your Chameleon password!"
Please ensure there is a chameleon_password() function
(which prints your Chameleon Cloud password) available
from your current shell and sub-shells.

For example:

  chameleon_password() {
    echo \"password\"
  }
  # export for use in sub-shells
  export -f chameleon_password

The function will be passed the name of the cloud as
its first argument, e.g. "chi_uc".

NOPASSWD
  exit 1
fi

docker_options=(--rm --interactive --tty)
docker_options+=(-e "OS_USERNAME=$CHAMELEON_USER")
docker_options+=(-e "OS_PASSWORD=$password")
docker_options+=(-e "OS_CLOUD=$cloud")
docker_options+=(-v "$PWD:/host")
if [[ -z "${1:-}" ]]; then
  cmd="bash"
fi

exec docker run "${docker_options[@]}" "$registry/cc-openstack" "${cmd:-$@}"
