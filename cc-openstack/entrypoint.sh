#!/usr/bin/env bash
source /var/lib/cc/venv/bin/activate

# Ensure important OS_ vars are set as a convenience
# for older OpenStack CLI interfaces
set -a
source <(clouds2rc "$OS_CLOUD")
set +a

exec "$@"
