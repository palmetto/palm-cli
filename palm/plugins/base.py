import importlib
from typing import List, Optional, Tuple
from pathlib import Path
from urllib.parse import urlparse
from palm.utils import is_cmd_file, cmd_name_from_file, run_on_host


class BasePlugin:
    def __init__(
        self,
        name: str,
        command_dir: Path,
        version: Optional[str] = "unknown",
        package_location: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Initialize a plugin.

        Args:
            name (str): Name of the plugin
            command_dir (Path): Path to the directory containing commands
            version (Optional[str], optional): Plugin version. Defaults to "unknown".
            package_location (Optional[str], optional): Either pypi package name
                or github https URL. Used for installation Defaults to None.
        """
        self.name = name
        self.command_dir = command_dir
        self.version = version
        self.package_location = package_location
        self.__dict__.update(kwargs)

    def all_commands(self) -> List:
        """Get the commands for a plugin.

        Returns:
            list: List of click cli command names
        """
        command_list = []

        for path in self.command_dir.glob('*.py'):
            if is_cmd_file(path.name):
                command_list.append(cmd_name_from_file(path.name))

        return command_list

    def command_map(self) -> dict:
        """Returns a dict that maps all commands to the plugin name.
        Used by PluginManager to identify which plugin a command belongs to.

        Returns:
            dict: dict where key is command name and value is plugin name
        """
        return dict.fromkeys(self.all_commands(), self.name)

    def get_command(self, command_name: str) -> importlib.machinery.ModuleSpec:
        """Get the modulespec for a given command

        Args:
            command_name (str): Name of the command

        Returns:
            importlib.ModuleSpec: ModuleSpec for the command
        """
        command_path = self.command_dir / f'cmd_{command_name}.py'
        return importlib.util.spec_from_file_location(command_name, command_path)

    def update(self) -> Tuple[bool, str]:
        """Update the plugin.

        Returns:
            Tuple[bool, str]: Tuple of ('success', 'message')
        """
        if self.package_location is None:
            return (False, 'This plugin does not support upgrading via palm')

        package_url = urlparse(self.package_location)
        if package_url.hostname == 'github.com':
            install_url = f'git+{self.package_location}'
        else:  # This should be a pypi package name
            install_url = self.package_location

        # TODO: do a better job of the package name, prepend 'palm-' isn't great.
        uninstall_cmd = f"python3 -m pip uninstall -y palm-{self.name}"
        upgrade_cmd = f"python3 -m pip install {install_url}"

        for cmd in (uninstall_cmd, upgrade_cmd):
            _, _, _ = run_on_host(cmd, check=True)
        return (True, 'Plugin upgraded successfully')
