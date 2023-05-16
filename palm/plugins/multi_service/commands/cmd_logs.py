from typing import Optional
import click


@click.command("logs")
@click.option("--container", "-c", help="Container to get logs from")
@click.option("--follow", '-f', is_flag=True, help="Don't wrap command in /bin/bash -c")
@click.option("-tail", '-n', default=50, help="Number of lines to tail, defaults to 50. Use 0 for all lines.")
@click.pass_obj
def cli(environment, container: Optional[str], follow: bool, tail: int):
    """Tail logs from a container"""

    if tail == 0:
        tail = 'all'

    cmd = ['docker logs', '-n', str(tail)]

    if follow:
        cmd.append('-f')

    if not container:
        plugin = environment.get_plugin('multi_service')
        container = plugin.pick_service()

    cmd.append(container)

    click.secho(f'Viewing logs from {container}...', fg='yellow')
    environment.run_on_host(' '.join(cmd), check=True)
