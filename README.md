# climeleon

_CLI interface(s) for Chameleon operators._

This provides a new tool called `chi` that can make some operational tasks
easier, namely through:

  - Reducing the overhead required to ssh/scp on to specific machines
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
# export CHAMELEON_SSH_ID="~/.ssh/id_chameleon" # Defaults to id_rsa if not set

# export TACC_USER="<username>" # Defaults to $USER
# export TACC_SSH_ID="<path/to/id>" # Defaults to $CHAMELEON_SSH_ID
# export TACC_JUMP_HOST="<fqdn of jump host>" # Defaults to staff.chameleon.tacc.utexas.edu

# export UC_USER="<user@uchicago.edu>"
# export UC_SSH_ID="<path/to/id>" # Defaults to $CHAMELEON_SSH_ID

# export MCS_USER="<user@uchicago.edu>"
# export MCS_SSH_ID="<path/to/id>" # Defaults to $CHAMELEON_SSH_ID
# export MCS_JUMP_HOST="<fqdn of jump host>" # Defaults to login.mcs.anl.gov

# export CELS_USER="<user@uchicago.edu>"
# export CELS_SSH_ID="<path/to/id>" # Defaults to $CHAMELEON_SSH_ID
# export CELS_JUMP_HOST="<fqdn of jump host>" # Defaults to logins.cels.anl.gov

# export NU_USER="<username>" # Defaults to $USER
# export NU_SSH_ID="<path/to/id>" # Defaults to $CHAMELEON_SSH_ID
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

In order to log in to the various nodes, sometimes it's necessary to log in as
various different user names. This can be controlled via the following env
variables:

  * `ANL_USER`: Argonne user account name
  * `TACC_USER`: TACC user account name (usually also your Chameleon one)
  * `UC_USER`: UChicago user account name
  * `CHAMELEON_USER`: Chameleon user account name

## Commands

### `docs`

This is a little convenience tool that currently just searches the (public)
Chameleon docs for a term and shows you which pages matched. Just saves a
browser window trip.

```
# Find doc pages referencing baremetal nodes
chi docs search "baremetal"
```

### `replacekey`

This is a convenience utility for updating your SSH public key on all
authentication servers. It works by simply taking you through a tour of all the
login servers we use and then updating your `~/.ssh/authorized_keys` to contain
a key you provide to the script. If it's your first time doing this, you will
have to enter your password several times, as no key exists on the server for
you yet and you'll have to fall back to password authentication.

```
# Note: this will replace all your existing public keys on the servers with the
# key you provide!
chi replacekey "/path/to/public/key"
```

### `ssh`/`scp`

This is a wrapper for SSH/SCP that handles authentication and the proxying of
connections via login nodes for you.

```
# Log in to a TACC node
chi ssh chameleon01.tacc.utexas.edu

# Log in to a UC node
chi ssh admin01.uc.chameleoncloud.org

# Log in to an internal-only node
# (Notice the use of -t to allocate a pseudo-tty)
chi ssh -t master2.chameleon.tacc.utexas.edu sudo ssh m01-03

# Also works with SCP
chi scp my-script.sh admin01.uc.chameleoncloud.org:

# Copy file between two sites (use -3 flag)
chi scp -3 admin01.uc.chameleoncloud.org:my-script.sh master2.chameleon.tacc.utexas.edu:
```

It is also possible to download the SSH config that makes this utility work, in
case you want to install it permanently.

```
chi ssh config >>~/.ssh/config
```

### `openstack` (and legacy OpenStack clients)

> **Note**: requires Docker.

The default behavior of `chi` is to select a cloud configuration for you and then
go on to running whatever command you wanted. This is accomplished via a Docker
container that has all of the dependencies already baked in.

```
# Run an `openstack` command against CHI@TACC
chi tacc openstack project list

# Run a `blazar` command against CHI@UC
chi uc blazar host-list
```

You can also spawn an interactive shell that has access to all of these
commands:

```
chi uc
```

### `vault`

This is a helper to interface with the Nimbus team vault hosted in MCS.

```
# Log in to the Vault (logins should persist for a bit)
chi vault login

# Search for a particular password, in this case "zenodo"
chi vault search zenodo

# Read a password
chi vault read <path>

# Update a password
chi vault write <path> value=<value>
```
