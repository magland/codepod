# Codepod

Open and/or develop project repositories in docker containers.

## Prerequisites

* Install git, docker and python 3 (>=3.6).
* Install pyyaml (pip install pyyaml)

## Installation from PyPI

```
pip install codepod
# for subsequent updates:
pip install --upgrade codepod
```

### Install from this repository
```
# After cloning this repository
cd codepod
pip install .
# for subsequent updates, pull changes, then:
pip install --upgrade .
```

## Basic usage

```
codepod [repository_name] <options>
<or>
codepod -w [workspace directory] <options>
```

For example, to open the codepod project itself:
```
git clone https://github.com/magland/codepod
codepod -w $PWD/codepod
```

This will create a container with the workspace mounted at `/home/project`, and place you within a bash shell in the terminal. The source files may be edited either inside the container or outside the container on the local (host) machine. Programs in the project should be executed inside the container, because that's where the development environment is set up.

To launch vscode within the container, run:

```
code .
```

A shortcut command (that automatically clones the repository into a temporary directory):

```
codepod https://github.com/magland/codepod
```

## Configuring the codepod environment for your project

Inspired by the gitpod project, codepod uses a .codepod.yml for configuration. If no .codepod.yml file exists, the default configuration will be used.

An example .codepod.yml file:

```
image: "docker_user/codepod_custom"
tasks:
- command: ./init.sh
```

If a custom image is used (optional), it should be based on one of the default codepod docker images. The default is `magland/codepod` on dockerhub.

Upon startup of the codepod container, the task commands are run sequentially.

## Mounting volumes

Mounting volumes is docker style using the `-v` option. For example:

```
codepod -w [workspace] -v /disk1/data:/data
```

## Using a custom docker image for the environment

TODO: write this section

## Mounting git credentials in the codepod container

TODO: write this section

## Authors

Jeremy Magland
