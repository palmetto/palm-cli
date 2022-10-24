import click


@click.command("lint")
@click.pass_obj
def cli(environment):
    """lint the codebase with black"""
    environment.run_in_docker(
        'black --skip-string-normalization --exclude="\.tpl\.py" .'
    )
