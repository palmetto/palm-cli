import click


@click.command('shell')
@click.pass_context
def cli(ctx):
    """Bash into your docker image to run arbitrary commands"""
    ctx.obj.run_in_docker('bash')
