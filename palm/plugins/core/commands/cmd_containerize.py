import click
from palm.palm_exceptions import AbortPalm
from palm.project_setup_utils import *


@click.command("containerize")
@click.pass_context
def cli(ctx):
    """Implement containerization for the current project

    Assumes basic python project structure.
    Uses docker and docker-compose to implement basic containerization
    Uses either requirements.txt or poetry to install dependencies
    
    """

    project_name = ctx.obj.palm.image_name
    package_manager = which_package_manager()

    if has_containerization():
        click.secho(f"This project appears to be containerized already", fg="red")
        return

    if not has_env():
        try:
            optionally_create_env()
        except AbortPalm:
            click.secho("Aborting containerization", fg="red")
            return

    if package_manager == "unknown":
        try:
            optionally_add_requirements_txt()
        except AbortPalm:
            click.secho("Aborting containerization", fg="red")
            return
        package_manager = "pip3"

    template_dir = Path(Path(__file__).parents[1], "templates") / "containerize"
    target_dir = Path.cwd()
    replacements = {
        "project_name": project_name,
        "package_manager": package_manager,
    }

    ctx.obj.generate(template_dir, target_dir, replacements)

    make_executable(Path(target_dir, "scripts", "entrypoint.sh"))

    click.secho(f"Containerization complete!", fg="green")
