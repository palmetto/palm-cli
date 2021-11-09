==============
Write a plugin
==============

Hello there, friend! Thank you in advance for your interest in writing a plugin for 
Palm CLI! If you have questions or want to discuss your ideas, please feel free to
contact the Core team at <data-analytics-team@palmetto.com>

.. TODO: DATA-423: Update this documentation with plugin generation instructions

Getting started
===============

At the time of writing, the process for creating a new plugin is not well defined.
We intend to implement a plugin generator in the near future, which will enable 
you to create the boilerplate for a plugin with very little effort. Given this 
planned feature will change documentation in the near future, we have decided to
keep documentation minimal at this time.

The shape of a plugin
=====================

- A Plugin is a python module that follows a set of conventions and provides an instance 
  of a Plugin that is loadable by the Palm CLI Plugin manager.
- The plugin module must use setuptools to be installable. setup.py must include:
    - A name that matches ``palm-{{name}}``
    - packages=find_namespace_packages(include=['palm', 'palm.*']),
    - install_requires=['palm>=2.0.0'],
- An ``__init__.py`` file must be present at ``palm/plugins/{{name}}/__init__.py``
- The ``__init__.py`` must include a ``Plugin`` variable which is an instance of
  the palm BasePlugin class, or an instance of a subclass of the BasePlugin class.
- The current convention is to create a ``/commands`` directory as a sibling of the
  plugin module. This directory must also contain an ``__init__.py`` file. This is
  where you will create the plugin's commands.

Installing your plugin during local development
===============================================

When developing a new plugin, it can be very useful to install your plugin
so that you can test it out. To do this, run the following command from
your plugin's root directory

.. code:: bash
  
  python3 -m pip install .
