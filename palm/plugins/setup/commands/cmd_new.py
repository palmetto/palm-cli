import click
import sys
from pathlib import Path


@click.command("new")
@click.option(
    '--global-template', '-g', help='Name of a global cookecutter template to use'
)
@click.option('--template', '-t', help='Cookie cutter template to use')
@click.option('--list', '-l', is_flag=True, help='List global cookiecutter templates')
@click.pass_obj
def cli(environment, global_template: str, template: str, list: bool = False):
    """
    Create a new project with cookiecutter.

    Cookiecutter is a command-line utility that creates projects from
    cookiecutters (project templates).

    This command will create a new project, in a new directory. You should
    run this command from the directory where you want the new project to
    be created.

    Global templates are defined in your global palm config file.
    See the docs for more information:
    https://palm-cli.readthedocs.io/en/latest/code-generation.html#new-projects-with-cookiecutter
    """
    if list:
        list_templates(environment)
        sys.exit(0)

    if global_template:
        default_cookiecutters = environment.palm.config.get('default_cookiecutters', {})
        template = default_cookiecutters.get(global_template)

    if not template:
        click.secho(f'No template defined for type {global_template}', fg='red')
        template = click.prompt('Please enter a cookiecutter template url')

    click.secho(f'Creating new {template} project', fg='green')

    ex_code, _, _ = environment.run_on_host(f'cookiecutter {template}')

    if ex_code == 0:
        click.secho(f'Project created!', fg='green')
    else:
        click.secho(f'Failed to create project', fg='red')
        sys.exit(1)


def list_templates(environment):
    """List global cookiecutter templates"""
    default_cookiecutters = environment.palm.config.get('default_cookiecutters', {})
    click.secho('Global cookiecutter templates:', fg='green')
    for key in default_cookiecutters.keys():
        click.echo(f'  {key}: {default_cookiecutters[key]}')
