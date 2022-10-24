import click


@click.command("test")
@click.pass_obj
def cli(environment):
    """Run tests for your application (pytest)"""
    click.echo("test command running!")
    environment.run_in_docker("pytest", {"PALM_TEST": True})
