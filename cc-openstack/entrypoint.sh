#!/usr/bin/env bash
export VIRTUAL_ENV_DISABLE_PROMPT=1
source /var/lib/cc/venv/bin/activate

# Ensure important OS_ vars are set as a convenience
# for older OpenStack CLI interfaces
set -a
source <(clouds2rc "$OS_CLOUD")
set +a

exec "$@"
