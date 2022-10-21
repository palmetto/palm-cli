from pathlib import Path
from palm.plugins.base import BasePlugin

SetupPlugin = BasePlugin(
    name='setup',
    command_dir=Path(__file__).parent / 'commands',
)
