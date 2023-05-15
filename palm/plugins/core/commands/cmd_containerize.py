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
@click.pass_context
def cli(ctx, version: str):
    if ctx.obj.palm.is_multi_service:
        click.secho(
            "Multi-service projects are not supported yet", fg="red", err=True
        )
        return

    all_templates_dir = Path(Path(__file__).parents[1], "templates")
    template_dir = all_templates_dir / "containerize"
    PythonContainerizer(ctx, template_dir, version).run()
    click.secho(f"Containerized {ctx.obj.palm.image_name}", fg="green")
