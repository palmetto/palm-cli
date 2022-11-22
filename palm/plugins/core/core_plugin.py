from pathlib import Path
from palm.plugins.base import BasePlugin

CorePlugin = BasePlugin(
    name='core',
    command_dir=Path(__file__).parent / 'commands',
)
