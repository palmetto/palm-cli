import click


@click.command('{{command}}')
@click.pass_context
def cli(ctx):
    """{{command}}"""
    click.echo("{{command}} command running!")
