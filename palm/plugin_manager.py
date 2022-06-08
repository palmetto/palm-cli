import importlib
from typing import List
from .plugins.base import BasePlugin as Plugin
from click import secho


class PluginManager:
    def __init__(self) -> None:
        self.plugins = {}
        self.plugin_command_dict = {}

    def load_plugins(self, plugins: List) -> None:
        """Loads a list of plugins, typically from palm config

        Args:
            plugins (list): list of plugin names to load
        """
        for plugin in plugins:
            self.load_plugin(plugin)

    def load_plugin(self, plugin_name: str) -> Plugin:
        """Load a single plugin by name

        Args:
            plugin_name (str): name of the plugin to be loaded

        Raises:
            KeyError: Raised if the requested plugin is not available

        Returns:
            Plugin: Plugin instance
        """
        try:
            module: Plugin = importlib.import_module('.' + plugin_name, 'palm.plugins')
        except ModuleNotFoundError as e:
            if e.name == 'palm.plugins.' + plugin_name:
                secho(f'Could not find plugin: {plugin_name}!', fg='red')
            secho(f'Error importing plugin: {e}', fg='red')
            raise

        plugin = module.Plugin
        self.plugins[plugin_name] = plugin
        self.extend_plugin_command_mapping(plugin_name)

        return plugin

    def extend_plugin_command_mapping(self, plugin_name: str) -> None:
        """Merges the plugin commands to the PluginManager plugin_command_dict
        Note that this is using dict merging. In the event of 2 plugins having the
        same command name, the second command will supercede the first, replacing it.

        Args:
            plugin_name (str): name of the plugin
        """
        self.plugin_command_dict = {
            **self.plugin_command_dict,
            **self.plugins[plugin_name].command_map(),
        }

    def is_plugin_command(self, command_name: str) -> bool:
        """Check whether a given command name comes from a plugin

        Args:
            command_name (str): Name of the palm command

        Returns:
            bool: True if the command name is registered by a plugin
        """
        return command_name in self.plugin_command_list

    def command_spec(self, command_name) -> importlib.machinery.ModuleSpec:
        """Get the executable module spec for the plugin command

        Args:
            command_name (str): Name of the palm command

        Returns:
            ModuleSpec: ModuleSpec of the command being executed
        """
        plugin_name = self.plugin_command_dict[command_name]
        plugin = self.plugins[plugin_name]
        return plugin.get_command(command_name)

    @property
    def plugin_command_list(self) -> List:
        """Get all commands for installed plugins

        Returns:
            list: List of all commands for installed plugins
        """
        return list(self.plugin_command_dict.keys())
