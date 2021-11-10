# Palm CLI Changelog

## 2.0.1

> 11/10/2021

Updates to configuration and package name due to an unexpected naming conflict in
pypi

## 2.0.0

> 11/10/2021

This major version marks our first open-source release, and thus the first version
with a changelog entry!

### Features

- **Plugins** commands for Palm CLI are now largely driven by a plugin architecture.
All commands in Palm are made available by one of several plugins. The core
plugin and repo plugin are part of the Palm-cli repository and provide global commands
as well as commands defined within the project's .palm directory. Additional plugins
such as palm-dbt can be installed on the user's machine and configured for use 
on a per-project basis. See the plugin section of the docs for more information
- **Palm config** Palm now reads a config.yaml file from the current project's .palm
directory. This configuration enables the plugin architecture and allows us more
flexibility around protecting specific branches and determining the docker image
name.
- **Dependency detection** Since docker is a core requirement for using Palm, we
added checks to ensure docker and docker-compose are installed and running.
- **Documentation** Palm documentation has been enhanced with readthedocs, and now
includes standard documentation for OSS projects, e.g. Contribution guide, code of conduct,
and this changelog!
- **Test suite** Palm now has a good baseline of test coverage!

### Improvements

- **General cleanup** - Code was reformatted for PEP8 compliance
- **Naming** - Renamed `run_in_shell` to `run_in_docker`, run_in_shell will be
deprecated in a future version.

### Bug fixes
