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

        return plugin_config

    def write_config(self, config: dict):
        palm_config = yaml.load(self.config_path.read_text(), Loader=yaml.FullLoader)
        if not 'plugin_config' in palm_config.keys():
            palm_config['plugin_config'] = {}
        palm_config['plugin_config'][self.plugin_name] = config
        self.config_path.write_text(yaml.dump(palm_config))