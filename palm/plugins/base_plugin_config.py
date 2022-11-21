from abc import ABC, abstractmethod
import click
from pathlib import Path
import yaml

class BasePluginConfig(ABC):
    def __init__(self, plugin_name: str):
        self.plugin_name = plugin_name
        self.config_path = Path.cwd() / ".palm" / f"config.yaml"

    @abstractmethod
    def set_config(self) -> bool:
        """Setter for plugin config

        This method should be implemented by the plugin to set the config
        for the plugin. It should return True if the config was set successfully,
        and False if it was not.

        Implementations of this method should call self.write_config to write
        the config to the config file.

        Returns:
            bool: True if config was set successfully, False if not
        """
        pass

    @abstractmethod
    def validate_config(self, config: dict) -> bool:
        """Validation method for plugin config

        This method should be implemented by the plugin to validate the config.
        Called before reading and writing the config file.
        Reading an invalid config will return an empty dict.
        Writing an invalid config will not write to the config file.

        Args:
            config (dict): The config to validate

        Returns:
            bool: Returns True if the config is valid, False otherwise
        """
        pass

    def get_config(self) -> dict:
        if not self.config_path.exists():
            click.secho(
                f"Config file not found at {self.config_path}, run palm init",
                fg="red"
            )
            return {}

        return self.read_config()

    def read_config(self) -> dict:
        palm_config = yaml.load(self.config_path.read_text(), Loader=yaml.FullLoader)
        plugin_config = palm_config.get('plugin_config', {}).get(self.plugin_name, {})

        if not plugin_config:
            self.set_config()

        if not self.validate_config(plugin_config):
            click.secho("Invalid plugin config", fg="red")
            return {}

        return plugin_config

    def write_config(self, config: dict):
        palm_config = yaml.load(self.config_path.read_text(), Loader=yaml.FullLoader)
        if not 'plugin_config' in palm_config.keys():
            palm_config['plugin_config'] = {}

        if not self.validate_config(config):
            click.secho("Invalid config, not writing to config file", fg="red")
            return

        palm_config['plugin_config'][self.plugin_name] = config
        self.config_path.write_text(yaml.dump(palm_config))