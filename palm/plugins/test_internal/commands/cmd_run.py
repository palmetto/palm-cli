import click


@click.command("run")
def cli():
    """no-op command used for testing only..."""
    click.secho('completed', fg='green')
