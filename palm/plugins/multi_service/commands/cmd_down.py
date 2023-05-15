import click


@click.command("down")
@click.argument("flags", nargs=-1)
@click.pass_obj
def cli(environment, flags: tuple):
    """Bring up all services"""
    # This sucks. Don't commit this.
    flags = [f"-{flag}" if len(flag) == 1 else f"--{flag}" for flag in flags]
    command = f'docker compose down {" ".join(flags)}'

    environment.run_on_host(command, check=True)
