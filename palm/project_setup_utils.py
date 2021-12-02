import os
from pathlib import Path
import click
from palm.palm_exceptions import AbortPalm


def has_env() -> bool:
    """Check for a .env file in the project root"""
    return Path(".env").exists()


def optionally_create_env():
    """Optionally, create a .env file if it doesn't exist

    Raises:
        AbortPalm: abort if the user doesn't want to create a .env file
    """
    create_env = click.confirm("Would you like palm to create an empty .env file?")
    if create_env:
        Path(".env").touch()
        click.secho(
            "Created an empty .env - please add your ENV vars there", fg="green"
        )
    else:
        raise AbortPalm("Aborting")


def make_executable(path: Path) -> None:
    """Make a file executable

    Args:
        path (Path): Path to file
    """
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(path, mode)
