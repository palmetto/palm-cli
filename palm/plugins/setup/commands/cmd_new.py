import click
import sys
from pathlib import Path

@click.command("new")
@click.option('--project_type', '-p', help='The type of project to create')
@click.option('--template', '-t', help='Cookie cutter template to use')
@click.option('--list', '-l', is_flag=True, help='List global cookiecutter templates')
@click.pass_obj
def cli(enviornment, project_type: str, template: str, list: bool = False):
    """Create a new project with cookiecutter"""
    if list:
        list_templates(enviornment)
        sys.exit(0)

    if project_type:
        default_cookiecutters = enviornment.palm.config.get('default_cookiecutters', {})
        template = default_cookiecutters.get(project_type)

    if not template:
        click.secho(f'No template defined for type {project_type}', fg='red')
        template = click.prompt('Please enter a cookiecutter template url')

    click.secho(f'Creating new {template} project', fg='green')

    ex_code, _, _ = enviornment.run_on_host(f'cookiecutter {template}')

    if ex_code == 0:
        click.secho(f'Project created!', fg='green')
    else:
        click.secho(f'Failed to create project', fg='red')
        sys.exit(1)

    dir = click.prompt('Please enter the directory of the project')
    if not Path(dir).exists():
        click.secho(f'Project directory {dir} does not exist', fg='red')
        click.secho(f'You will need to complete set up manually', fg='red')
        sys.exit(1)

    click.secho(f'Changing directory to {dir}', fg='green')
    ex_code, _, _ = enviornment.run_on_host(f'cd {dir}')
    enviornment.run_on_host('palm init')

    containerize = click.confirm('Would you like to containerize this project?')
    if containerize:
        enviornment.run_on_host('palm containerize')

def list_templates(enviornment):
    """List global cookiecutter templates"""
    default_cookiecutters = enviornment.palm.config.get('default_cookiecutters', {})
    click.secho('Global cookiecutter templates:', fg='green')
    for key in default_cookiecutters.keys():
        click.echo(f'  {key}: {default_cookiecutters[key]}')