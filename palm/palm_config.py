from pathlib import Path
from typing import Optional, List, Union
import yaml
from xmlrpc.client import Boolean
from pygit2 import Repository, discover_repository, GitError

from click import secho, echo
from deepmerge import always_merger
from pygit2 import Repository

from .palm_exceptions import NoRepositoryError


class PalmConfig:
    """Palm config class
    Reads the .palm/config.yaml from the current project
    Makes config available to other modules

    Args:
        project_root: The root path object if not cwd
    """

    project_root: Optional["Path"]
    config: dict = {}
    repo: Optional[Repository] = None
    branch: str = None
    plugins: List[str] = []

    def __init__(self, project_path: Optional["Path"] = Path.cwd()):
        self.project_root = project_path
        self._setup()

    def _setup(self):
        """Setup the config"""
        self.config = self._get_config()
        try:
            self.repo = self._get_repo()
        except NoRepositoryError:
            secho('No git repository found, running in global mode', fg='yellow')
            self.repo = None
        if self.repo:
            self.branch = self._get_current_branch()
            self._use_repo_plugins()
        else:
            self._use_global_plugins()

    def _get_repo(self) -> Repository:
        """Gets the repo object.

        Returns:
            Repository: repo object
        """
        path = discover_repository(str(self.project_root))

        if not path:
            raise NoRepositoryError("No git repository found in the current directory")

        return Repository(path)

    def _get_current_branch(self) -> Union[str, None]:
        """Gets the current branch name.

        Returns:
            Union[str, None]: branch name, or None if not in a repo
        """
        if self.repo:
            try:
                return self.repo.head.shorthand
            except GitError as e:
                secho('Error finding an active branch.', fg='red')
                echo(
                    'If this is a new repo, you should make an initial commit before using palm.\n'
                )
                raise e

        return None

    def _get_config(self) -> dict:
        """Gets both global and repo configs, merging them together.

        Returns:
            dict: dict of merged global and repo configs
        """
        return always_merger.merge(self._get_global_config(), self._get_repo_config())

    def _get_repo_config(self) -> dict:
        """Gets the repo config, reading yaml and returning a dict.
        If the config does not exist, prompt the user to create it.

        Returns:
            dict: dict of repo config, or empty dict if no config
        """
        config_path = self.project_root / ".palm" / "config.yaml"
        if not config_path.exists():
            secho(
                "No palm config found in .palm/config.yml, please run 'palm scaffold config'",
                fg="yellow",
            )
            secho(
                "Some palm commands may not work correctly without palm config \n",
                fg="yellow",
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
        config_path = global_config_path or Path().home() / ".palm" / "config.yaml"
        if not config_path.exists():
            self._create_global_config_file(config_path)

        return yaml.safe_load(config_path.read_text())

    def _create_global_config_file(self, config_path) -> None:
        """Creates the global config file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        default_config = {
            'plugins': [],
            'excluded_commands': [],
            'default_cookiecutters': {},
        }
        config_path.write_text(yaml.dump(default_config))

    def _use_repo_plugins(self):
        """Use the default plugins - core, plugins, and repo defined commands"""
        core_plugins = ['core']
        plugins_from_config = self.config.get('plugins') or []
        # The order here defines the order in which commands will be overridden
        # Plugins on the right will override plugins on the left!
        self.plugins = core_plugins + plugins_from_config + ['repo']

    def _use_global_plugins(self):
        """Use the setup plugins - when palm is used outside of a git repo"""
        global_plugins = ['setup']
        plugins_from_config = self.config.get('plugins') or []

        self.plugins = global_plugins + plugins_from_config

    def is_valid_branch(self) -> Boolean:
        """Validate the current branch against the config

        Return:
            Boolean: True if the branch is valid, False if not
        """
        if self.repo and self.branch in self.protected_branches:
            return False

        return True

    @property
    def protected_branches(self) -> List[Optional[str]]:
        """Returns the list of configured protected branches for the current repo

        Returns:
             list[Optional[str]]: list of branch names e.g ['main', 'master']
        """
        return self.config.get("protected_branches") or []

    @property
    def project_root_snake_case(self):
        return self.project_root.name.replace("-", "_")

    @property
    def image_name(self) -> str:
        """Docker image name for the current project
        Attempts to load the image_name from .palm/config.yaml, falling back to
        the snake_cased project root dir name

        Returns:
            str: Name of docker image to use
        """
        return self.config.get('image_name') or self.project_root_snake_case
