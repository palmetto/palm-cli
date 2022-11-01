import click


@click.command("shell")
@click.pass_obj
def cli(environment):
    """Bash into your docker image to run arbitrary commands"""
    environment.run_in_docker("bash")
