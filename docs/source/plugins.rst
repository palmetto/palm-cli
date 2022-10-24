=======
Plugins
=======

Palm plugins extend the functionality of the CLI. They usually add new commands
that are specific to a particular platform or framework. A plugin could also
share organization-specific functionality across multiple projects, or provide
a common base for a set of commands.

Core plugins
============

To simplify the CLI implementation, all Palm commands come from Plugins.
Within the Palm CLI repository, you will find a directory called "plugins" which
contains a set of plugins. The "core" and "repo" plugins are automatically loaded
when the CLI runs, these plugins provide the following functionality:

- core: Provides the core commands of Palm CLI.
- repo: Loads your custom commands from the ``.palm`` directory if available.

**Note** that the repo plugin does not provide any commands of its own, instead
it provides the mechanism to load your own project-specific commands.

Installing Plugins
==================

Palm plugins are installed as pypi packages. To install a plugin, install
the pypi package for the plugin in the same python path as Palm CLI.

e.g.
``pip install palm-dbt``

Configuring Plugins
====================

Once installed, you can configure your project to use a plugin by adding the
name of the plugin to the project's ``.palm/config.yaml`` file. See the plugin's
documentation for more information on how to configure each specific plugin.

Example plugin configuration

.. code:: yaml

  plugins:
    - dbt

Configuring Global Plugins
==========================

You can also configure plugins that are not specific to a project. This is
done by adding the name of the plugin to the ``~/.palm/config.yaml`` file in
the user's home directory. This global configuration file will be created the
first time palm is run.

Example global plugin configuration

.. code:: yaml

  plugins:
    - workflow
    - git


Using plugin commands
=====================

Once you have installed and configured a plugin, it's commands should be available
for use within the project. To confirm this and to explore the available commands
run ``palm --help`` to list the available commands in your project.

Keeping up to date
==================

As with all software, plugins are likely to change over time. To keep up to date,
palm provides some utility methods to check which version you are running and
update to the latest version if available.

- ``palm plugin versions`` to list all versions of configured plugins.
- ``palm plugin update --name <plugin_name>`` to update a specific plugin.
- ``palm plugin --help`` to see all plugin utility commands.

Writing your own plugins
========================

So, you have a set of commands that you want to re-use across projects?
Or, maybe you have a set of commands you want to share with other people?
Writing a plugin is a great way to contribute to the Palm CLI ecosystem.

Check out the :doc:'write-a-plugin' section to learn how to write your own plugin.
