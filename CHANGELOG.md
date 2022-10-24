# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [2.5.0]

### Added

- **Global palm** allows palm to run outside of initialized git projects.
  This feature opens up many new possibilities for automation with palm,
  including project scaffolding with cookiecutter, machine setup, and
  global plugins that can do just about anything!
- **Project scaffolding** with cookiecutter. Palm now includes cookiecutter
  for scaffolding new projects. Why would you use palm for this, instead of
  using cookiecutter directly? Because with palm, you're able to configure a set
  of default cookiecutter templates, which helps keep projects consistent.
  Every developer, on every team, should use the same set of templates!
- **Pre-commit** Added pre-commit hooks to palm to improve contributor
  experience.

### Changed

- **linting & cleanup** as a result of adding more tools in out pre-commit
  hooks, we also cleaned up some poorly formatted files in the project!.

## [2.4.1] - 2022-06-08

### Changed

- **Improved layout for palm --help**: Palm help now outputs the command list in
groups based on the plugin the command originates from! This is particularly helpful
when working in a project that defines uses plugins, defines it's own commands,
and you have global plugins installed!

### Fixed

- Fixed a path issue for windows users when using code_gen or palm init
- Fixes a potential security vulnerability when upgrading plugins via 
`palm plugin update`
- Fixes a number of other small issues detected by CodeQL static anlysis

## [2.4.0] - 2022-04-10

### Added

- **Run docker commands without /bin/bash** - Added optional arguments to
environment.run_in_docker allows developers to execute commands in their docker
containers without prepending them with /bin/bash -c. This is useful & necessary
for images with a specific entrypoint
- **New documentation** for:
  - Global palm configuration
  - Shell autocomplete
  - Upgrading palm

## [2.3.0] - 2022-03-28


Features:

- **Override command** The new `palm override` command makes it easy to change the functionality of core or plugin commands in your project.
- **git repo added to palm config** Developers can now access the pygit2 Repository via the context.obj.palm.config - this can be helpful when implementing commands that use git or need data from the repo.

Improvements

- **Startup speed** changed the implementation of checking docker-compose is installed, this fixes intermittent slowdowns on startup
- **Dependency upgrades**: Click updated to v8.1 and up, Black updated to v22.3.0

## [2.2.0] - 2022-02.24

Python Version Support:

- **Dropped support for python3.6** Python 3.6 is end of life and supporting it started to cause issues with dependent packages. We are dropping support for python 3.6 in palm v2.2.0

### Added

- **Global config & Global plugins** Palm now supports installing plugins globally!
After updating to palm 2.2.0, the first time you run `palm ...` a new global config
will be created at `~/.palm/config.yaml`, you can add plugins to this config to
make them available to all of your repositories! This feature was developed to 
support a Palmetto internal `palm-workflow` plugin, which is used to manage our
dev workflow in Trello.

### Fixed

- **pygit2 version pin adjusted**: The upper version pin on pygit2 was removed to resolve an error
installing palm on newer versions of MacOS. Note that libgit2 is still required, 
per the requirements of pygit2. A future version will introduce checking for libgit2
and more friendly error messaging.
- **Upgraded jinja**: We were previously using an unsupported version of Jinja which was using
a deprecated method in markupsafe, markupsafe removed that method which caused an error when
installing palm. We upgraded to the latest version of jinja to resolve this issue and get the latest jinja features.

## [2.1.1] - 2022-02-07

### Fixed

- Resolve a template issue when running `palm plugin new` 

### Changed

- Command templates now use click's @pass_obj decorator and pass the `environment`
argument, this is a cleaner API for interacting with the Palm.Environment class
- CI now runs against multiple python versions
- Black version is pinned for consistency between local & CI runs

## [2.1.0] - 2021-12-01

Our first minor release on v2 includes containerization, support for older Python versions, 
and added logo and brand assets!

### Added

- **Containerize**: NEW command added for containerization of Python projects with `palm containerize`
- **Shell**: NEW command to shell into the project container and execute arbitrary commands
- **Plugin generator**: NEW command to generate the boilerplate code for writing a new plugin
- **Excluded commands**: Added the ability to exclude/disable `palm` commands from a project's config
- **`run_on_host`**: Added a new function, `ctx.obj.run_on_host`, to assist with developing new commands 
to run on your local machine, standardizing the interface around Python's `subprocess` with platform
and version agnostic support (well, version agnostic >= 3.6.9).
- **Logo/Branding**: We have a logo!! It is 90's retro and it is cool. Also added branding guidelines

### Changed

- **Command availability**: Added `lint` and `test` commands to the `palm` core plugin
- **Workflow**: New Github Actions workflow to lint contributions to the project on new Pull Request
- **Backwards compatibility**: Added backwards compatibility support for older Python versions through v3.6.9
- **Documentation**: Added new docs and examples of `palm` use cases and impact

## [2.0.2] - 2021-11-22

We acquired the name `palm` in pypi! This patch version is just renaming the library
and updating installation instructions.

## [2.0.1] - 11/10/2021

Updates to configuration and package name due to an unexpected naming conflict in
pypi

## [2.0.0] - 2021-11-10

This major version marks our first open-source release, and thus the first version
with a changelog entry!

### Added

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

### Changed

- **General cleanup** - Code was reformatted for PEP8 compliance
- **Naming** - Renamed `run_in_shell` to `run_in_docker`, run_in_shell will be
deprecated in a future version.
