# climeleon

_CLI interface(s) for Chameleon operators._

This provides a new tool called `chi` that can make some operational tasks
easier, namely through:

  - Standardizing the execution environment for Python OpenStack clients
  - Providing a means of adminstrating multiple OpenStack clouds with one
    tool

## Setup

You can build the Docker container(s) necessary and install some symlinks to
/usr/local/bin (configurable with CHI_INSTALL_PATH env variable) by running the
default `make` task.

```
make
```

### Credentials

The scripts need to use your credentials in order to call the OpenStack API. The
value of the `CHAMELEON_USER` environment variable will be used as your Chameleon
username, so ensure it is set. You can include it in your .bashrc, or place it into a
separate file and source it. For example:

```bash
# File named .chi.env
#! /bin/sh
export CHAMELEON_USER=my_cham_user
# Or, e.g., for users using Globus auth
export CHAMELEON_USER=my_email_address@example.com
```

The scripts additionally look for a function in your shell called `chameleon_password`,
which you should provide. If you do not have this function sourced you will be
notified and the script will bail. It is recommended that the function feature
some level of indirection, such as calling an external password manager to
retrieve your credentials. For example, LastPass provides a `lpass` binary to
assist. Mac OS X also has the `security` binary which acts as an intermediary to
the OS X Keychain.

### Cloud Configurations

You can pass a custom OpenStack configuration file (clouds.yaml)
to Climeleon with the `CHAMELEON_CONFIG` variable. If there is an associated
clouds-public.yaml, Climeleon will resolve it automatically.

If you manage multiple sites and have multiple OpenStack config files, you can
still use the `CHAMELEON_CONFIG` variable with a space-separated list of these files:

```
CHAMELEON_CONFIG="/path/to/file1 /path/to/file2 ..."
```

The default value of `CHAMELEON_CONFIG` is `$HOME/.config/chameleon/clouds.yaml`. 
This can be useful if you wish to manually concatenate your config files and/or only 
use the `CHAMELEON_CONFIG` variable for testing purposes.

Examples:

**Using LastPass**

```
chameleon_password() {
  echo "$(lpass --show --password chameleon)"
}
# Important: export for sub-shells
export -f chameleon_password
```

**Using 1Password**

```
chameleon_password() {
  echo "$(op get item chameleon \
    | jq '.details.fields[] | select(.designation=="password").value')"
}
# Important: export for sub-shells
export -f chameleon_password
```

**Using Bitwarden**

```
chameleon_password() {
  $(bw get password chameleon --raw)
}
# Important: export for sub-shells
export -f chameleon_password
```

## Commands

### `docs`

This is a little convenience tool that currently just searches the (public)
Chameleon docs for a term and shows you which pages matched. Just saves a
browser window trip.

```
# Find doc pages referencing baremetal nodes
chi docs search "baremetal"
```

### `openstack` (and legacy OpenStack clients)

> **Note**: requires Docker.

The default behavior of `chi` is to select a cloud configuration for you and then
go on to running whatever command you wanted. This is accomplished via a Docker
container that has all of the dependencies already baked in.

```
# Run an `openstack` command against <cloud>
chi <cloud> openstack project list

# Run a `blazar` command against <cloud>
chi <cloud> blazar host-list
```

You can also spawn an interactive shell that has access to all of these
commands:

```
chi <cloud>
```

