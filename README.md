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

The scripts need to use your credentials in order to call the OpenStack API and also log in to machines that use password authentication. To do this, the CLI expects to find two source functions called `tacc_credentials` and `uc_credentials`. If you do not have these functions sourced you will be notified and the script will bail. It is recommended that these functions feature some level of indirection, such as calling an external password manager to retrieve your credentials. For example, LastPass provides a `lpass` binary to assist. Mac OS X also has the `security` binary which acts as an intermediary to the OS X Keychain.

Example:

```
tacc_credentials() {
  # The output is expected to be username on line 1, password on line 2.
  echo "$(lpass --show --username tacc)"
  echo "$(lpass --show --password tacc)"
}
# Important: export for sub-shells
export -f tacc_credentials
```

## Commands

### `ssh`/`scp`

> **Note**: requires [`sshpass`](https://gist.github.com/arunoda/7790979). Normally using this binary is considered very bad security practice. However, in our case, it is reasonable because we are never executing this on a shared environment and your passwords are never sent directly as arguments--rather, they are sourced as temporary env variables bound to the execution of the sshpass process on your local machine. It is used mostly because we have several systems using password-based authentication.

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

