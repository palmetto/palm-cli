import click


@click.command("down")
@click.pass_obj
def cli(environment):
    """Bring up all services"""
    command = f'docker compose down'

    click.secho(f'Tearing down all services...', fg='yellow')
    environment.run_on_host(command, check=True)
