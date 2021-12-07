import click


@click.group()
def cli():
    """{{group}}"""
    pass


{% for command in commands %}
@cli.command()
@click.pass_obj
def {{command}}(environment):
    """{{command}}"""
    click.echo("{{command}} command running!")
    command = "echo {{command}} running" 
    # Run your command in docker:
    # environment.run_in_docker(command)
    # Or on the host:
    # environment.run_on_host(command)

{% endfor %}