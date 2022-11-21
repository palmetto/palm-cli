from abc import ABC, abstractmethod
import click
from pathlib import Path
import yaml
from pydantic import BaseModel, ValidationError

from palm.palm_exceptions import InvalidConfigError

class BasePluginConfig(ABC):
    def __init__(self, plugin_name: str, model: BaseModel):
        self.plugin_name = plugin_name
        self.config_path = Path.cwd() / ".palm" / f"config.yaml"
        self.model = model

    @abstractmethod
    def set(self) -> dict:
        """Setter for plugin config

        This method should be implemented by the plugin to set the config
        for the plugin. It should return True if the config was set successfully,
        and False if it was not.

        Implementations of this method should call self.write(config) to write
        the config to the config file.

        Returns:
            dict: The config that was set
        """
        pass

    def write(self, config: dict):
        palm_config = yaml.load(self.config_path.read_text(), Loader=yaml.FullLoader)
        if not 'plugin_config' in palm_config.keys():
            palm_config['plugin_config'] = {}

        if not self.validate(config):
            click.secho("Invalid config, not writing to config file", fg="red")
            raise InvalidConfigError

        palm_config['plugin_config'][self.plugin_name] = config
        self.config_path.write_text(yaml.dump(palm_config))


    def get(self) -> dict:
        if not self.config_path.exists():
            click.secho(
                f"Config file not found at {self.config_path}, run palm init",
                fg="red"
            )
            return {}

        return self._read()


    def _read(self) -> dict:
        palm_config = yaml.load(self.config_path.read_text(), Loader=yaml.FullLoader)
        plugin_config = palm_config.get('plugin_config', {}).get(self.plugin_name, {})

        if not plugin_config:
            plugin_config = self.set()

        if not self.validate(plugin_config):
            raise InvalidConfigError

        return plugin_config

    def validate(self, config: dict) -> bool:
        """Validates the plugin config against the pydantic model

        Args:
            config (dict): The config to validate

        Returns:
            bool: Returns True if the config is valid, Raises InvalidConfigError if not
        """
        try:
            self.model(**config)
            return True
        except ValidationError as e:
            msg = f"Invalid config for plugin {self.plugin_name}: {e}"
            raise InvalidConfigError(msg)