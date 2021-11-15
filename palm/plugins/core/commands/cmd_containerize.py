import click
from pathlib import Path
from palm.containerizer import PythonContainerizer


@click.command("containerize")
@click.pass_context
def cli(ctx):
    template_dir = Path(Path(__file__).parents[1], "templates") / "containerize"
    PythonContainerizer(ctx, ctx.obj.palm.image_name, template_dir).run()
    click.secho(f"Containerized {ctx.obj.palm.image_name}", fg="green")
