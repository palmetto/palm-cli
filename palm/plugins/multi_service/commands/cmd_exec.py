from typing import Optional
import click


@click.command("exec")
@click.option("--command", "-cmd", required=True, help="Command to execute")
@click.option("--container", "-c", help="Container to get logs from")
@click.option("--no-bin-bash", is_flag=True, help="Don't wrap command in /bin/bash -c")
@click.pass_obj
def cli(environment, command: str, container: Optional[str], no_bin_bash: bool):
    """Exec a command within a running container"""

    cmd = ['docker exec -it']

    if not container:
        plugin = environment.get_plugin('multi_service')
        container = plugin.pick_service()

    cmd.append(container)

    if not no_bin_bash:
        cmd.append('/bin/bash -c')

    cmd.append(command)
    click.secho(f'Running {command} in {container}...', fg='yellow')

    environment.run_on_host(' '.join(cmd), check=True)
