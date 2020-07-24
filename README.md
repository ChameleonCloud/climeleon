# climeleon

_CLI interface(s) for Chameleon operators._

This provides a new tool called `cc` that can make some operational tasks easier, namely through:

  - Reducing the overhead required to ssh/scp on to specific machines
  - Standardizing the execution environment for Python OpenStack clients
  - Providing a set of default OpenStack client configurations and a means of easily swapping them out.

## Setup

You can build the Docker container(s) necessary and install some symlinks to /usr/local/bin (configurable with CC_INSTALL_PATH env variable) by running the default `make` task.

```
make
```

### Credentials

The scripts need to use your credentials in order to call the OpenStack API. To do this, it looks for a function in your shell called `chameleon_password`, which you should provide. If you do not have this function sourced you will be notified and the script will bail. It is recommended that the function feature some level of indirection, such as calling an external password manager to retrieve your credentials. For example, LastPass provides a `lpass` binary to assist. Mac OS X also has the `security` binary which acts as an intermediary to the OS X Keychain.

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
  echo "$(op get item chameleon | jq '.details.fields[] | select(.designation=="password").value')"
}
# Important: export for sub-shells
export -f chameleon_password
```

In order to log in to the various nodes, sometimes it's necessary to log in as various different user names. This can be controlled via the following env variables:

  * `ANL_USER`: Argonne user account name
  * `TACC_USER`: TACC user account name (usually also your Chameleon one)
  * `UC_USER`: UChicago user account name
  * `CHAMELEON_USER`: Chameleon user account name

## Commands

### `docs`

This is a little convenience tool that currently just searches the (public) Chameleon docs for a term and shows you which pages matched. Just saves a browser window trip.

```
# Find doc pages referencing baremetal nodes
cc docs search "baremetal"
```

### `replacekey`

This is a convenience utility for updating your SSH public key on all authentication servers. It works by simply taking you through a tour of all the login servers we use and then updating your `~/.ssh/authorized_keys` to contain a key you provide to the script. If it's your first time doing this, you will have to enter your password several times, as no key exists on the server for you yet and you'll have to fall back to password authentication.

```
# Note: this will replace all your existing public keys on the servers with the key you provide!
cc replacekey "/path/to/public/key"
```

### `ssh`/`scp`

This is a wrapper for SSH/SCP that handles authentication and the proxying of connections via login nodes for you.

```
# Log in to a TACC node
cc ssh chameleon01.tacc.utexas.edu

# Log in to a UC node
cc ssh admin01.uc.chameleoncloud.org

# Log in to an internal-only node
# (Notice the use of -t to allocate a pseudo-tty)
cc ssh -t master2.chameleon.tacc.utexas.edu sudo ssh m01-03

# Also works with SCP
cc scp my-script.sh admin01.uc.chameleoncloud.org:

# Copy file between two sites (use -3 flag)
cc scp -3 admin01.uc.chameleoncloud.org:my-script.sh master2.chameleon.tacc.utexas.edu:
```

It is also possible to download the SSH config that makes this utility work, in case you want to install it permanently.

```
cc ssh config >>~/.ssh/config
```

### `openstack` (and legacy OpenStack clients)

> **Note**: requires Docker.

The default behavior of `cc` is to select a cloud configuration for you and then go on to running whatever command you wanted. This is accomplished via a Docker container that has all of the dependencies already baked in.

```
# Run an `openstack` command against CHI@TACC
cc tacc openstack project list

# Run a `blazar` command against CHI@UC
cc uc blazar host-list
```

You can also spawn an interactive shell that has access to all of these commands:

```
cc uc
```

### `vault`

This is a helper to interface with the Nimbus team vault hosted in MCS.

```
# Log in to the Vault (logins should persist for a bit)
cc vault login

# Search for a particular password, in this case "zenodo"
cc vault search zenodo

# Read a password
cc vault read <path>

# Update a password
cc vault write <path> value=<value>
```
