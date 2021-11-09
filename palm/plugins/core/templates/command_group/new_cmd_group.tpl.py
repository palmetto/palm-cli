import click


@click.group()
def cli():
    """{{group}}"""
    pass


{% for command in commands %}
@cli.command()
@click.pass_context
def {{command}}(ctx):
    """{{command}}"""
    click.echo("{{command}} command running!")

{% endfor %}