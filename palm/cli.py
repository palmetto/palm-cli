import sys
import click
import importlib
import os
import pkg_resources
from pathlib import Path
from typing import Optional, Any, Callable, List

from .environment import Environment
from .palm_config import PalmConfig
from .plugin_manager import PluginManager
from .utils import is_cmd_file, cmd_name_from_file, run_on_host

CONTEXT_SETTINGS = dict(auto_envvar_prefix="PALM")

plugin_manager_instance = PluginManager()
palm_config = PalmConfig()


class PalmCLI(click.MultiCommand):
    def __init__(
        self,
        name: Optional[str] = None,
        invoke_without_command: bool = None,
        no_args_is_help: Optional[bool] = None,
        subcommand_metavar: Optional[str] = None,
        chain: bool = None,
        result_callback: Optional[Callable[..., Any]] = None,
        **attrs: Any,
    ) -> None:
        try:
            palm_config.validate_branch()
        except SystemExit as e:
            sys.exit(1)
        self.palm = palm_config
        self.plugin_manager = plugin_manager_instance
        self.plugin_manager.load_plugins(self.palm.plugins)

        super().__init__(
            name=name,
            invoke_without_command=invoke_without_command,
            no_args_is_help=no_args_is_help,
            subcommand_metavar=subcommand_metavar,
            chain=chain,
            result_callback=result_callback,
            **attrs,
        )

    def _commands_from_dir(self, dir) -> List[str]:
        commands = []
        for filename in os.listdir(dir):
            if is_cmd_file(filename):
                commands.append(cmd_name_from_file(filename))
        return commands

    def list_commands(self, ctx) -> List[str]:
        cmds = self.plugin_manager.plugin_command_list
        dedupe = set(cmds)
        cmds = list(dedupe)
        cmds.sort()
        project_excluded_commands = self.palm.config.get('excluded_commands', [])
        cmds = filter(lambda x: x not in project_excluded_commands, cmds)
        return cmds

    def get_command(self, ctx, cmd_name: str) -> click.Command:
        try:
            if self.plugin_manager.is_plugin_command(cmd_name):
                spec = self.plugin_manager.command_spec(cmd_name)
            else:
                raise FileNotFoundError
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        except ImportError as error:
            click.secho(f'Import error: {error}', fg="red")
            return
        except FileNotFoundError:
            click.secho('Command not found, check spelling!', fg="red")
            return
        return mod.cli


def get_version():
    try:
        version = pkg_resources.require("palm")[0].version
    except pkg_resources.DistributionNotFound:
        version = 'unknown'
    return version


def required_dependencies_ready():

    docker_checks = (
        (
            "docker --version",
            "Docker is not installed, please install it first",
        ),
        (
            "docker-compose --version",
            "Docker Compose is not installed, please install it first",
        ),
        (
            "docker ps",
            "Docker is not running, please start it first",
        ),
    )
    for cmd, msg in docker_checks:
        if run_on_host(cmd, capture_output=True)[0] > 0:
            click.secho(msg, fg="red")
            return False
    return True


@click.group(cls=PalmCLI, context_settings=CONTEXT_SETTINGS)
@click.version_option(get_version())
@click.pass_context
def cli(ctx):
    """Palmetto data product command line interface."""
    is_test = os.getenv("PALM_TEST")
    if not (is_test or required_dependencies_ready()):
        ctx.exit(1)
    ctx.obj = Environment(plugin_manager_instance, palm_config)


if __name__ == "__main__":
    cli()
