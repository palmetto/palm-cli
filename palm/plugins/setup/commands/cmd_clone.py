import click
import subprocess


@click.command("clone")
def cli():
    """Clone and setup a project"""
    subprocess.run(["echo", "palm clone"], check=True)
