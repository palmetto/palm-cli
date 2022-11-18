import yaml

from abc import ABC, abstractmethod
from pathlib import Path

class BasePluginConfig(ABC):
    def __init__(self, plugin_name: str):
        self.plugin_name = plugin_name
        self.config_path = Path.cwd() / ".palm" / f"{plugin_name}_config.yaml"

    @abstractmethod
    def set_config(self) -> bool:
        pass

    def get_config(self):
        if not self._ensure_config():
            return {}

        return yaml.load(self.config_path.read_text(), Loader=yaml.FullLoader)

    def write_config(self, config: dict):
        self.config_path.write_text(yaml.dump(config))

    def _ensure_config(self) -> bool:
        if not self.config_path.exists():
            return self.set_config()
        return True