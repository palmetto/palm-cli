from typing import Optional
import click
from pathlib import Path
from palm.plugins.core.create_files import *

palm_target_dir = f'{Path.cwd()}/.palm'
templates_dir = Path(Path(__file__).parents[1], "templates").resolve()


@click.command()
@click.option("-i", "--image-name", multiple=False, help="Name of your docker image")
@click.option("-p", "--plugins", multiple=True, help="List of plugins you want to use")
@click.option(
    "-pb",
    "--protected-branches",
    multiple=True,
    help="Branches you do not want to run palm on",
)
@click.option(
    "-c", "--commands", multiple=True, help="List of command names to scaffold"
)
@click.pass_context
def cli(
    ctx,
    image_name: Optional[str],
    plugins: Optional[tuple],
    protected_branches: Optional[tuple],
    commands: Optional[tuple],
):
    """
    Initialize the project for use with Palm

    Creates the .palm directory with __init__.py
    Creates .palm/config.yaml with image_name, plugins, and protected_branches
    based on the options provided
    Creates command files based on the --commands option
    """
    template_dir = Path(Path(__file__).parents[1], "templates") / 'command'

    if Path(palm_target_dir).exists():
        click.secho("Palm is already initialized", fg="red")
        return

    Path('.palm').mkdir()
    Path('.palm/__init__.py').touch()

    for command in commands:
        click.echo(f'Adding template for {command}...')
        create_command(ctx, command, template_dir, palm_target_dir)

    if not image_name:
        image_name = ctx.obj.palm.image_name

    create_config(palm_target_dir, image_name, plugins, protected_branches)

    click.secho('Success! Project initialized with Palm CLI', fg='green')
