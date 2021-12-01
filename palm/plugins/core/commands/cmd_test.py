import click


@click.command('test')
@click.pass_context
def cli(ctx):
    """Run tests for your application (pytest)"""
    click.echo("test command running!")
    ctx.obj.run_in_docker('pytest', {'PALM_TEST': True})
