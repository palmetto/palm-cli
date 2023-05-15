import click


@click.command("logs")
@click.option("--container", "-c", help="Container to get logs from")
@click.option("--follow", '-f', is_flag=True, help="Don't wrap command in /bin/bash -c")
@click.pass_obj
def cli(environment, container: str, follow: bool):
    """Tail logs from a container"""

    cmd = ['docker logs']

    if follow:
        cmd.append('-f')

    if not container:
        services = environment.palm.docker_details.service_names
        container = environment.choice_prompt(
            "Which container would you like to get logs from?",
            services
        )

    cmd.append(container)

    environment.run_on_host(' '.join(cmd), check=True)
