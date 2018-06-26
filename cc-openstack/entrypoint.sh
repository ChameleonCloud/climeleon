#!/usr/bin/env bash
set -e -u -o pipefail

# Ensure important OS_ vars are set as a convenience
# for older OpenStack CLI interfaces
set -a
source <(clouds2rc "$OS_CLOUD")
set +a

exec "$@"
