from pathlib import Path

from palm.plugins.multi_service.multi_service_config import MultiServicePluginConfig
from palm.plugins.base import BasePlugin

MultiServicePlugin = BasePlugin(
    name="multi_service",
    command_dir=Path(__file__).parent / "commands",
    config=MultiServicePluginConfig(),
)
