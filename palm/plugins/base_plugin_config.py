from abc import ABC, abstractmethod
import click
from pathlib import Path
import yaml
from pydantic import BaseModel, ValidationError

class BasePluginConfig(ABC):
    def __init__(self, plugin_name: str, model: BaseModel):
        self.plugin_name = plugin_name
        self.config_path = Path.cwd() / ".palm" / f"config.yaml"
        self.model = model

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

    def validate_config(self, config: dict) -> bool:
        """Validates the plugin config against the pydantic model

        Args:
            config (dict): The config to validate

        Returns:
            bool: Returns True if the config is valid, False otherwise
        """
        try:
            self.model(**config)
            return True
        except ValidationError as e:
            click.secho(f"Invalid config for plugin {self.plugin_name}", fg="red")
            click.echo(e)
            return False

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