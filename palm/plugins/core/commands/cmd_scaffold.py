from pathlib import Path
from typing import List, Optional

import click

from palm.plugins.core.create_files import *

palm_target_dir = f"{Path.cwd()}/.palm"


@click.group(help="Scaffold new palm commands")
def cli():
    pass


@cli.command()
@click.option(
    "-n",
    "--name",
    multiple=True,
    required=True,
    help="Name of the command(s) you are adding",
)
@click.pass_obj
def command(environment, name: List[str]):
    template_dir = Path(Path(__file__).parents[1], "templates") / 'command'
    """Add a new palm command to the current repo"""
    for command in name:
        create_command(environment, command, template_dir, palm_target_dir)
        click.secho(f"{command} command created in {palm_target_dir}", fg="green")


@cli.command()
@click.option(
    "--group", multiple=False, required=True, help="Name of the command group"
)
@click.option(
    "-c",
    "--command",
    multiple=True,
    required=True,
    help="Name of the commands within the command group",
)
@click.pass_obj
def group(environment, group: str, command: List[str]):
    """Add a new palm command group to the current repo"""
    template_path = Path(Path(__file__).parents[1], "templates") / "command_group"
    replacements = {
        "group": group,
        "commands": command,
    }

    environment.generate(template_path, palm_target_dir, replacements)
    click.secho(f"{group} command group created in {palm_target_dir}", fg="green")


@cli.command("config")
@click.option("-i", "--image-name", multiple=False, help="Name of your docker image")
@click.option("-p", "--plugins", multiple=True, help="List of plugins you want to use")
@click.option(
    "-pb",
    "--protected-branches",
    multiple=True,
    help="List of branches you do not want to run palm on",
)
@click.pass_obj
def config(
    environment,
    image_name: Optional[str],
    plugins: Optional[tuple],
    protected_branches: Optional[tuple],
):
    """Generate a base .palm/config for existing projects"""
    image_name = image_name or environment.palm.image_name
    create_config(palm_target_dir, image_name, plugins, protected_branches)
    click.secho("Palm config created!", fg="green")
