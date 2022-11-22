===================
High-level Features
===================

Run in docker
=============

Palm and docker are like peas in a pod. Docker containers allow us to run our
commands in a sandboxed environment that is isolated from the rest of the system
and is a close reflection of our production and CI environments. Docker ensures
that everyone on your team is using a consistent OS and set of dependencies.
We're not here to sell you on Docker, and we don't expect you to be a Docker pro,
but you will need Docker in order to work with Palm.


Local commands
==============

Palm allows you to define commands within each of your projects, and then share
them across your team. Once you have set up your project to use Palm, you can
create new commands in the ``.palm`` directory, add these to version control and
they will be available to everyone on your team when they run ``palm``.

See the :doc:`commands` section for more information.

Code generation
===============

Palm includes code generation functionality, powered by jinja. Code generation
allows you to automate repetitive boiler plating tasks, and keep your codebase
consistent. Code generation is driven by the ``environment.generate()`` function.

See the :doc:`code-generation` section for more information.


Plugins
=======

Palm is extensible. You can install plugins that extend the functionality of Palm.
Adding commands for specific frameworks or project types is a common use case.
Once installed, plugins must be configured for use with your project.

See the :doc:`plugins` section for more information.

