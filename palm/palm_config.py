from pathlib import Path
from typing import Optional, List
from pygit2 import Repository
from click import secho
import yaml


class PalmConfig:
    """Palm config class
    Reads the .palm/config.yaml from the current project
    Makes config available to other modules

    Args:
        project_root: The root path object if not cwd
    """

    branch: str = None

    def __init__(self, project_path: Optional["Path"] = Path.cwd()):
        self.project_root = project_path
        self.config = self._get_config()
        self.branch = self._get_current_branch()

    def _get_current_branch(self) -> str:
        return Repository(str(self.project_root)).head.shorthand

    def _get_config(self) -> object:
        config_path = self.project_root / '.palm' / 'config.yaml'
        if not config_path.exists():
            secho(
                'No palm config found in .palm/config.yml, please run \'palm scaffold config\'',
                fg='yellow',
            )
            secho(
                'Some palm commands may not work correctly without palm config',
                fg='yellow',
            )
            return {}

        return yaml.safe_load(config_path.read_text())

    def validate_branch(self) -> None:
        """Raises SystemExit if branch is protected."""
        if self.branch not in self.protected_branches:
            return
        msg = f"You are currently on protected branch {self.branch}. For your safety Palm will not run!"
        secho(msg, fg="red")
        raise SystemExit(msg)

    @property
    def has_config(self) -> bool:
        return len(self.config.keys()) > 0

    @property
    def protected_branches(self) -> List[Optional[str]]:
        """Returns the list of configured protected branches for the current repo

        Returns:
             list[Optional[str]]: list of branch names e.g ['main', 'master']
        """
        return self.config.get('protected_branches') or []

    @property
    def project_root_snake_case(self):
        return self.project_root.name.replace('-', '_')

    @property
    def image_name(self) -> str:
        """Docker image name for the current project
        Attempts to load the image_name from .palm/config.yaml, falling back to
        the snake_cased project root dir name

        Returns:
            str: Name of docker image to use
        """
        return self.config.get('image_name') or self.project_root_snake_case

    @property
    def plugins(self) -> list:
        core_plugins = ['core']
        plugins_from_config = self.config.get('plugins') or []
        # The order here defines the order in which commands will be overridden
        # Plugins on the right will override plugins on the left!
        return core_plugins + plugins_from_config + ['repo']
