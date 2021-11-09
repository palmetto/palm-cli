import click
import subprocess
from pathlib import Path
import webbrowser

CODE_DOCS_URI = "http://localhost:8989"


@click.command('docs')
@click.pass_context
def cli(ctx):
    """Generates internal readthedocs for palm and serves them"""

    click.echo(f"Launching palm-cli readthedocs at {CODE_DOCS_URI}...")
    subprocess.run(
        'docker-compose run --detach --rm --service-ports palm_docs',
        cwd=Path.cwd(),
        shell=True,
        check=True,
    )
    webbrowser.open_new_tab(CODE_DOCS_URI)
