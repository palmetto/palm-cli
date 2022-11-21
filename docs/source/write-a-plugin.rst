==============
Write a plugin
==============

Hello there, friend! Thank you in advance for your interest in writing a plugin for
Palm CLI! If you have questions or want to discuss your ideas, please feel free to
contact the Core team at <data-analytics-team@palmetto.com>


Getting started
===============

Palm includes a command to generate a plugin skeleton. You can use it to get started.

1. cd into an active project - this is necessary at the moment as palm commands
   are not currently available outside of an initialized git repository.
2. Run ``palm plugin new --name <plugin-name>`` and follow the prompts.
3. Your new plugin skeleton is created and ready for you to add commands!

Installing your plugin during local development
===============================================

When developing a new plugin, you will want to install your plugin
so that you can test it out.  To do this, run the following command from
your plugin's root directory:

.. code:: bash

  python3 -m pip install .

**Note**: Due to the way plugins are used by palm, you will need to re-install
the plugin every time you want to test changes to the plugin

Creating a Plugin Config
========================

If you wantto make your plugin configurable, you will need to create a plugin
config object and provide it to the plugin constructor.

The plugin config object:
- must be a subclass of ``palm.plugins.base_plugin_config.BasePluginConfig``
- must define a ``set`` method which returns a dictionary of config values
- must be initialized with a model object, using the pydantic ``BaseModel``,
  which defines the config schema and will be used to validate the config values.

Here is an example of a plugin config object and how to use it in a plugin:

.. code:: python

  import click
  from palm.plugins.base import BasePlugin
  from palm.plugins.base_plugin_config import BasePluginConfig
  from pydantic import BaseModel

  # Define the config schema
  class MyPluginConfigModel(BaseModel):
      my_config_value: str

  # Define the config object
  class MyPluginConfig(BasePluginConfig):
      def __init__(self):
          super().__init__('my_plugin', MyPluginConfigModel)

      def set(self):
          return {
              "my_config_value": click.prompt("Please enter a value for my_config_value", type=str)
          }

  # Create the plugin, providing the config object
  my_plugin = BasePlugin(name='my_plugin', config=MyPluginConfig())

Using Plugin Config values
--------------------------

To use the config values in your plugin's commands, a ``plugin_config`` method
is provided on the environment object. This method takes the name of the plugin
and returns the config values for that plugin.

Here is an example of how to use the plugin config values in a plugin command:

.. code:: python

  @click.command()
  @click.pass_obj
  def my_command(environment):
      plugin_config = env.plugin_config('my_plugin')
      my_config_value = plugin_config.get('my_config_value', '')
      click.echo(f"my_config_value is {my_config_value}")
