import click


@click.command('{{command}}')
@click.pass_obj
def cli(environment):
    """{{command}}"""
    click.echo("palm executing {{command}}")
    command = f"echo '{{command}} running!'"
    # Run your command in docker:
    # environment.run_in_docker(command)
    # Or on the host:
    # environment.run_on_host(command)
