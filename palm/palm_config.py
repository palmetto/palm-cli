from pathlib import Path
from typing import Optional, List
from pygit2 import Repository
from click import secho
from deepmerge import always_merger
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
        self.repo = self._get_repo()
        self.branch = self._get_current_branch()

    def _get_repo(self) -> Repository:
        """Gets the repo object.

        Returns:
            Repository: repo object
        """
        return Repository(str(self.project_root))

    def _get_current_branch(self) -> str:
        return self.repo.head.shorthand

    def _get_config(self) -> object:
        """Gets both global and repo configs, merging them together.

        Returns:
            object: dict of merged global and repo configs
        """
        return always_merger.merge(self._get_global_config(), self._get_repo_config())

    def _get_repo_config(self) -> object:
        """Gets the repo config, reading yaml and returning a dict.
        If the config does not exist, prompt the user to create it.

        Returns:
            object: dict of repo config, or empty dict if no config
        """
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

    def _get_global_config(self, global_config_path: Optional[Path] = None) -> object:
        """Gets the global config, reading yaml and returning a dict.
        If the config does not exist, create it.

        Args:
            global_config_path (Optional[Path], optional): Used for testing. Defaults to None.

        Returns:
            object: dict of global config
        """
        config_path = global_config_path or Path().home() / '.palm' / 'config.yaml'
        if not config_path.exists():
            self._create_global_config_file(config_path)

        return yaml.safe_load(config_path.read_text())

    def _create_global_config_file(self, config_path) -> None:
        """Creates the global config file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        default_config = {
            'plugins': [],
            'excluded_commands': [],
        }
        config_path.write_text(yaml.dump(default_config))

    def validate_branch(self) -> None:
        """Raises SystemExit if branch is protected."""
        if self.branch not in self.protected_branches:
            return
        msg = f"You are currently on protected branch {self.branch}. For your safety Palm will not run!"
        secho(msg, fg="red")
        raise SystemExit(msg)

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
