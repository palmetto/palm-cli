import click


@click.command("up")
@click.option(
    "--no-detach", "-nd", is_flag=True, help="Do not run containers in the background."
)
@click.option(
    "--build", "-b", is_flag=True, help="Build images before starting containers."
)
@click.pass_obj
def cli(environment, no_detach: bool, build: bool):
    """Bring up all services"""

    command = 'docker compose up'
    if not no_detach:
        command += ' -d'
    if build:
        command += ' --build'

    click.secho(f'Bringing up all services...', fg='yellow')
    environment.run_on_host(command, check=True)
