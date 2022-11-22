import webbrowser
from pathlib import Path

import click

CODE_DOCS_URI = "http://localhost:8989"


@click.command("docs")
@click.pass_obj
def cli(environment):
    """Generates internal readthedocs for palm and serves them"""

    click.echo(f"Launching palm-cli readthedocs at {CODE_DOCS_URI}...")
    exit_code, out, err = environment.run_on_host(
        "docker-compose run -d --rm --service-ports palm_docs"
    )
    if exit_code > 0:
        if "port is already allocated" in err:
            click.secho(
                (
                    "It looks like palm docs (or something else) "
                    "is already running on port 8989. Aborting."
                ),
                fg="yellow",
            )
        return
    webbrowser.open_new_tab(CODE_DOCS_URI)
