import subprocess
from sys import version_info
from typing import Optional, Tuple, List

import click


class UnsupportedVersion(Exception):
    pass


def is_cmd_file(filename: str) -> bool:
    return filename.endswith(".py") and filename.startswith("cmd")


def cmd_name_from_file(filename: str) -> str:
    return filename[4:-3]


def run_on_host(
    cmd: str,
    check: Optional[bool] = False,
    capture_output: Optional[bool] = False,
) -> Tuple[int, str, str]:
    """A simplifed, platform-and-version agnostic interface
    for subprocess.
    By default run_on_host makes some strong
    conventional choices:
     - calls are run as a shell
     - calls are blocking
     - errors in the shell are NOT bubbled up by default
    Args:
        cmd: the command to run.
        check: if True raise a CalledProcessError
        capture_output: if True, stdout and stderr will be suppressed
    Returns:
        Tuple: status code, stdout, stderr

    """
    major, minor, patch, _, _ = version_info
    kwargs = dict(shell=True, check=check)
    if major < 3 or minor < 5:
        raise UnsupportedVersion(f"Python version {major}.{minor} is not supported.")
    if minor < 7:
        from subprocess import PIPE

        if capture_output:
            kwargs.update(dict(stdout=PIPE, stderr=PIPE))
    else:
        kwargs.update(dict(capture_output=capture_output))

    completed = subprocess.run(cmd, **kwargs)
    return (
        completed.returncode,
        completed.stdout.decode("utf-8") if completed.stdout else "",
        completed.stderr.decode("utf-8") if completed.stderr else "",
    )


def run_in_docker(
    cmd: str,
    image_name: str,
    env_vars: Optional[List[str]] = [],
    no_bin_bash: Optional[bool] = False,
    capture_output: Optional[bool] = False,
    silent: Optional[bool] = False,
) -> Tuple[bool, str]:
    """Shells out and runs the cmd in docker

    Args:
        cmd (str): The command you want to run
        env_vars (Optional[dict], optional): Dict of env vars to pass to the docker container.
    """
    if not silent:
        click.secho(f"Executing command `{cmd}` in compose...", fg="yellow")

    docker_cmd = ["docker compose run --service-ports --rm"]
    docker_cmd.extend(env_vars)
    docker_cmd.append(image_name)
    if no_bin_bash:
        docker_cmd.append(cmd)
    else:
        docker_cmd.append(f'/bin/bash -c "{cmd}" ')

    ex_code, std_out, std_err = run_on_host(" ".join(docker_cmd), False, capture_output)
    if capture_output:
        if ex_code == 0:
            return (True, std_out)
        return (False, std_err)

    if ex_code == 0:
        return (True, "Success! Palm completed with exit code 0")
    return (False, f"Fail! Palm exited with code {ex_code}")
