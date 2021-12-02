import click
from pathlib import Path
from palm.containerizer import PythonContainerizer


@click.command("containerize")
@click.option(
    "--version",
    multiple=False,
    default="3.8",
    help="Python version to use (default 3.8)",
)
@click.pass_context
def cli(ctx, version: str):
    template_dir = Path(Path(__file__).parents[1], "templates") / "containerize"
    PythonContainerizer(ctx, template_dir, version).run()
    click.secho(f"Containerized {ctx.obj.palm.image_name}", fg="green")
