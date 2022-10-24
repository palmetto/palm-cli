from pathlib import Path

import click

from palm.containerizer import PythonContainerizer


@click.command("containerize")
@click.option(
    "--version",
    multiple=False,
    default="3.8",
    help="Python version to use (default 3.8)",
)
@click.pass_obj
def cli(environment, version: str):
    all_templates_dir = Path(Path(__file__).parents[1], "templates")
    template_dir = all_templates_dir / "containerize"
    PythonContainerizer(environment, template_dir, version).run()
    click.secho(f"Containerized {environment.palm.image_name}", fg="green")
