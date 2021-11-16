import click
import subprocess


@click.command("new-machine")
def cli():
    """Initial setup for your machine"""
    subprocess.run(["echo", "setup"], check=True)
