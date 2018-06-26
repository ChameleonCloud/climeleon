# climeleon

_CLI interface(s) for Chameleon operators._

This provides a new tool called `cc` that can make some operational tasks easier, namely through:

  - Reducing the overhead required to get on to specific machines
  - Standardizing the execution environment for Python OpenStack clients
  - Providing a set of default OpenStack client configurations and a means of easily swapping them out.

## Setup

You can build the Docker container(s) necessary and install some symlinks to /usr/local/bin (configurable with CC_INSTALL_PATH env variable) by running the default `make` task.

```
$> make
```

## Commands

### `ssh`

> **Note**: requires [`sshpass`](https://gist.github.com/arunoda/7790979). Normally using this binary is considered very bad security practice. However, in our case, it is reasonable because we are never executing this on a shared environment and your passwords are never sent directly as arguments--rather, they are sourced as temporary env variables bound to the execution of the sshpass process on your local machine. It is used mostly because we have several systems using password-based authentication.

This is a wrapper for SSH that handles authentication and the proxying of connections via login nodes for you.

```
# Log in to a TACC node
$> cc ssh chameleon01.tacc.utexas.edu

# Log in to a UC node
$> cc ssh admin01.uc.chameleoncloud.org

# Log in to an internal-only node
# (Notice the use of -t to allocate a pseudo-tty)
$> cc ssh master2.chameleon.tacc.utexas.edu -t sudo ssh m01-03
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

