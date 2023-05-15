import click


@click.command("build")
@click.pass_obj
def cli(environment):
    """Rebuilds the image for the current working directory"""

    command = f'docker compose build {environment.palm.image_name}'
    environment.run_on_host(command, check=True)
