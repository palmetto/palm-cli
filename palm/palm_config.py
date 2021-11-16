from pathlib import Path
from typing import Optional, List
from pygit2 import Repository, discover_repository
from click import secho
import yaml

from .palm_exceptions import NoRepositoryError


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
        self.branch = ''
        self.plugins = []
        self.use_default_plugins()

    def validate_branch(self) -> None:
        """Validate the current branch against the config

        Raises:
            NoRepositoryError: If there is no git repository in the current directory
            SystemExit: If the branch is listed as protected in the config
        """
        try:
            branch = self._get_current_branch()
        except NoRepositoryError as e:
            raise e
        
        self.branch = branch
        if branch not in self.protected_branches:
            return
        msg = f"You are currently on protected branch {branch}. For your safety Palm will not run!"
        secho(msg, fg="red")
        raise SystemExit(msg)

    def use_default_plugins(self):
        """Use the default plugins - core, plugins, and repo defined commands"""
        core_plugins = ['core']
        plugins_from_config = self.config.get('plugins') or []
        # The order here defines the order in which commands will be overridden
        # Plugins on the right will override plugins on the left!
        self.plugins = core_plugins + plugins_from_config + ['repo']

    def use_setup_plugins(self):
        """Use the setup plugins - when palm is used outside of a git repo"""
        self.plugins = ['setup']

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

    def _get_current_branch(self) -> str:
        path = discover_repository(self.project_root)

        if not path:
            raise NoRepositoryError("No git repository found in the current directory")
        
        return Repository(path).head.shorthand

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
