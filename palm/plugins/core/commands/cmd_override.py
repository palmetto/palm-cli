import click
import shutil
from pathlib import Path


@click.command('override')
@click.option('--name', multiple=False, required=True, help='Name of the command')
@click.pass_obj
def cli(environment, name: str):
    """Override a command in the current project"""
    spec = environment.plugin_manager.command_spec(name)
    origin_path = Path(spec.origin)
    file_name = origin_path.name
    target_path = Path(environment.palm.project_root, '.palm', file_name)

    if target_path.exists():
        click.secho('Command already exists in project, skipping', fg='red')
        return

    if not target_path.parent.exists():
        click.secho(
            "palm is not initialized in this project, please run 'palm init' first",
            fg='red',
        )
        return

    shutil.copy(origin_path, target_path)
    click.secho(f"{name} command overridden to {target_path}", fg='green')
