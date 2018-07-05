# climeleon

_CLI interface(s) for Chameleon operators._

This provides a new tool called `cc` that can make some operational tasks easier, namely through:

  - Reducing the overhead required to ssh/scp on to specific machines
  - Standardizing the execution environment for Python OpenStack clients
  - Providing a set of default OpenStack client configurations and a means of easily swapping them out.

## Setup

You can build the Docker container(s) necessary and install some symlinks to /usr/local/bin (configurable with CC_INSTALL_PATH env variable) by running the default `make` task.

```
$> make
```

### Credentials

The scripts need to use your credentials in order to call the OpenStack API and also ensure you can SSH to each site, which often involves authenticating as users with different names. To do this, the CLI expects to find two source functions called `tacc_credentials` and `uc_credentials`. If you do not have these functions sourced you will be notified and the script will bail. It is recommended that these functions feature some level of indirection, such as calling an external password manager to retrieve your credentials. For example, LastPass provides a `lpass` binary to assist. Mac OS X also has the `security` binary which acts as an intermediary to the OS X Keychain.

Examples:

**Using LastPass**

```
tacc_credentials() {
  # The output is expected to be username on line 1, password on line 2.
  echo "$(lpass --show --username tacc)"
  echo "$(lpass --show --password tacc)"
}
# Important: export for sub-shells
export -f tacc_credentials
```

**Using 1Password**

```
tacc_credentials() {
  # The output is expected to be username on line 1, password on line 2.
  echo "$(op get item tacc | jq '.details.fields[] | select(.designation=="username").value')"
  echo "$(op get item tacc | jq '.details.fields[] | select(.designation=="password").value')"
}
# Important: export for sub-shells
export -f tacc_credentials
```

## Commands

### `replacekey`

This is a convenience utility for updating your SSH public key on all authentication servers. It works by simply taking you through a tour of all the login servers we use and then updating your `~/.ssh/authorized_keys` to contain a key you provide to the script. If it's your first time doing this, you will have to enter your password several times, as no key exists on the server for you yet and you'll have to fall back to password authentication.

```
# Note: this will replace all your existing public keys on the servers with the key you provide!
$> cc replacekey "/path/to/public/key"
```

### `ssh`/`scp`

This is a wrapper for SSH/SCP that handles authentication and the proxying of connections via login nodes for you.

```
# Log in to a TACC node
$> cc ssh chameleon01.tacc.utexas.edu

# Log in to a UC node
$> cc ssh admin01.uc.chameleoncloud.org

# Log in to an internal-only node
# (Notice the use of -t to allocate a pseudo-tty)
$> cc ssh -t master2.chameleon.tacc.utexas.edu sudo ssh m01-03

# Also works with SCP
$> cc scp my-script.sh admin01.uc.chameleoncloud.org:
```

### `openstack` (and legacy OpenStack clients)

> **Note**: requires Docker.

The default behavior of `cc` is to select a cloud configuration for you and then go on to running whatever command you wanted. This is accomplished via a Docker container that has all of the dependencies already baked in.

```
# Run an `openstack` command against CHI@TACC
$> cc CHI@TACC openstack project list

# Run a `blazar` command against CHI@UC
$> cc CHI@UC blazar host-list
```

