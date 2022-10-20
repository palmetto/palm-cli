import click
import subprocess


@click.command("new")
def cli():
    """Create a new project"""
    subprocess.run(["echo", "palm new"], check=True)