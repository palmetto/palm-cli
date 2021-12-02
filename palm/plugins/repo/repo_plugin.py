from pathlib import Path
from palm.plugins.base import BasePlugin

RepoPlugin = BasePlugin(
    name='repo',
    command_dir=Path.cwd() / '.palm',
)
