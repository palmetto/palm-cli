import click


@click.command('lint')
@click.pass_context
def cli(ctx):
    """lint the codebase with black"""
    ctx.obj.run_in_docker('black --skip-string-normalization --exclude="\.tpl\.py" .')
