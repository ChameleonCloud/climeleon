#!/usr/bin/env sh

# Get Stored Token
STORED_TOKEN=$(security find-generic-password -a "$USER" -s 'op_token' -w)
TOKEN=$(op signin my -r --session "$STORED_TOKEN")
# Update stored token
security add-generic-password -a "$USER" -s 'op_token' -w "$TOKEN" -U
op get item chameleoncloud.org --fields password --session="$TOKEN"
