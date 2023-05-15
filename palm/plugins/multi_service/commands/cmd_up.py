import click


@click.command("up")
@click.option("--detach", "-d", is_flag=True, help="Run containers in the background.")
@click.option("--build", "-b", is_flag=True, help="Build images before starting containers.")
@click.pass_obj
def cli(environment, detach: bool, build: bool):
    """Bring up all services"""

    command = 'docker compose up'
    if detach:
      command += ' -d'
    if build:
      command += ' --build'

    environment.run_on_host(command, check=True)
