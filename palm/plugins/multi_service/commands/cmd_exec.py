from typing import Optional
import click


@click.command("exec")
@click.option("--command", "-cmd", required=True, help="Command to execute")
@click.option("--container", "-c", help="Container to get logs from")
@click.option("--no-bin-bash", is_flag=True, help="Don't wrap command in /bin/bash -c")
@click.pass_obj
def cli(environment, command: str, container: Optional[str], no_bin_bash: bool):
    """Exec a command within a running container"""

    environment.exec_in_docker(command, container=container, no_bin_bash=no_bin_bash)
