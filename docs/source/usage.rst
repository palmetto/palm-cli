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

``pip install palmcli``

For development installations, you may also install palm from source by cloning
the codebase and running ``python3 -m pip install .``

To verify that the installation was successful, run ``palm --version``.


**note for mac users**: if you get this warning::

  WARNING: The script palm is installed in '/Users/yourname/Library/Python/3.8/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

you will need to add ``'/Users/yourname/Library/Python/3.8/bin'`` to your path for 
``palm`` to work. You can do that with one of these commands (depending on your
shell of choice):

- zsh: ``echo "\nexport PATH=$PATH:/Users/yourname/Library/Python/3.8/bin\n" >> ~/.zprofile``
- bash: ``echo "export PATH=$PATH:/Users/yourname/Library/Python/3.8/bin" >> ~/.bashrc``
- fsh: ``echo "setenv PATH $PATH:/Users/yourname/Library/Python/3.8/bin" >> ~/.fshrc``

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
