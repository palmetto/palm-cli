import click


@click.command("build")
@click.option("--service", "-s", help="Service to build (for multi-service projects)")
@click.pass_obj
def cli(environment, service: str):
    """Rebuilds the image for the current working directory.

    For multi-service projects, you can specify a service to build with the -
    -service flag. Otherwise, you will rebuild all services.
    """

    if service and environment.palm.is_multi_service:
        command = f'docker compose build {service}'
    else:
        command = f'docker compose build'

    environment.run_on_host(command, check=True)
