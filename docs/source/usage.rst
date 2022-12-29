=====
Usage
=====

Palm CLI is a command line tool, once installed you can use palm by running
``palm`` from your terminal. If no command is provided, ``palm`` will render the
help text for commands in the current project

.. code:: bash

   > palm
   Usage: palm [OPTIONS] COMMAND [ARGS]...

   Palm command line interface.

   Options:
   --version  Show the version and exit.
   --help     Show this message and exit.

   Commands:
   build     Rebuilds the image for the current working directory
   docs      Generates internal readthedocs for palm and serves them
   plugin    Palm plugin utilities
   scaffold  Scaffold new palm commands
   update    This updates the current version of palm.


System Requirements
===================

Palm is designed to be OS agnostic and should work on Windows, Mac OS X, and
common Linux distributions.

Palm requires the following software to be installed and running on your
device:

1. `Docker <https://docs.docker.com/get-docker/>`_
   You can check to see if you already have it with ``docker --version``
2. `Python3 <https://www.python.org/downloads/>`_
   You can check to see if you already have it with ``python3 --version``


Installation
============

Install Palm CLI via pip:

``pip install palm``

For development installations, you may also install palm from source by cloning
the codebase and running ``python3 -m pip install .``

To verify that the installation was successful, run ``palm --version``.


**note for mac users**: if you get this warning::

  WARNING: The script palm is installed in '~/Library/Python/3.x/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

you will need to add ``'/Users/yourname/Library/Python/3.x/bin'`` to your path for
``palm`` to work. 

This command will work for bash, zsh and fsh shells:

``export PALM_INSTALL_LIB_AT=$(python3 --version | sed -e "s/\(Python 3\.\)\([0-9]\)\.\([0-9]\)/3.\2/") && echo "\nexport PATH=$PATH:$HOME/Library/Python/${PALM_INSTALL_LIB_AT}/bin\n" | tee -a ~/.zprofile ~/.bashrc ~/.fshrc``


Configuration
=============

To configure your project to use Palm, run ``palm init`` from the root
directory of your project.

This will walk you through setting up Palm for your project and create a ``/.palm``
directory containing a ``config.yaml`` - this is where you can make changes to your
project's Palm configuration.

**Configuration Options:**

- image_name: (str) the name of the docker image used to run your project
- plugins: (list) a list of plugins used by your project, plugins must be installed!
- protected_branches: (list) a list of github branches that palm will not run against

**Global palm configuration**

As of palm v2.2.0 palm also supports a global configuration file. This file is
automatically created at ``~/.palm/config.yaml`` and contains the following options:

- plugins: (list) a list of plugins used globally, plugins must be installed!
- excluded_commands: (list) a list of palm commands that you do not want to use.

Shell Completion
================

To enable autocomplete for palm commands, add one of the following shell-specific
lines to your shell's profile. Once added, either source your profile or start
a new shell session.

**zsh**:
``eval "$(_PALM_COMPLETE=zsh_source palm)"``

**bash**:
``eval "$(_PALM_COMPLETE=bash_source palm)"``

**fish**:
``eval "$(_PALM_COMPLETE=fish_source palm)"``

**Adding shell completion to your commands**

If you'd like to add/improve shell completion for your own commands, check out
the click documentation for `shell-completion <https://click.palletsprojects.com/en/8.0.x/shell-completion/#custom-type-completion>`_.
