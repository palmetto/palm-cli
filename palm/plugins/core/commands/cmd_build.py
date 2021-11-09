import click
import subprocess


@click.command("build")
def cli():
    """Rebuilds the image for the current working directory"""
    subprocess.run(["docker-compose", "build"], check=True)
