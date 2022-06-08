from typing import Optional, Tuple
import importlib
from pathlib import Path
from typing import Optional, List, Tuple
import click
from palm.utils import run_on_host
from palm.plugin_manager import PluginManager
from .palm_config import PalmConfig
from .code_generator import CodeGenerator


class Environment:
    def __init__(self, plugin_manager: PluginManager, palm_config: PalmConfig):
        self.home = Path.cwd()
        self.palm = palm_config
        self.plugin_manager = plugin_manager

    def run_in_docker(
        self,
        cmd: str,
        env_vars: Optional[dict] = {},
        no_bin_bash: Optional[bool] = False,
    ) -> Tuple[bool, str]:
        """Shells out and runs the cmd in docker

        Args:
            cmd (str): The command you want to run
            env_vars (Optional[dict], optional): Dict of env vars to pass to the docker container.
        """
        click.secho(f"Executing command `{cmd}` in compose...", fg="yellow")

        docker_cmd = ['docker-compose run --service-ports --rm']
        docker_cmd.extend(self._build_env_vars(env_vars))
        docker_cmd.append(self.palm.image_name)
        if no_bin_bash:
            docker_cmd.append(cmd)
        else:
            docker_cmd.append(f'/bin/bash -c "{cmd}" ')

        ex_code, _, _ = run_on_host(' '.join(docker_cmd))
        if ex_code == 0:
            return (True, 'Success! Palm completed with exit code 0')
        return (False, f"Fail! Palm exited with code {ex_code}")

    def run_in_shell(self, cmd: str, env_vars: Optional[dict] = {}):
        """deprecated - use run_in_docker"""

        deprecation_msg = (
            "DEPRECATION: run_in_shell has been renamed to "
            "`run_in_docker` and will be removed in a future version. "
            "Please update your commands to use ctx.obj.run_in_docker"
        )
        click.secho(deprecation_msg, fg="yellow")
        success, msg = self.run_in_docker(cmd, env_vars)
        click.secho(msg, fg="green" if success else "red")

    def run_on_host(
        self,
        cmd: str,
        check: Optional[bool] = False,
        capture_output: Optional[bool] = False,
    ) -> Tuple[int, str, str]:
        """context wrapper for :obj:`palm.utils.run_on_host`"""
        return run_on_host(cmd, check, capture_output)

    def import_module(self, module_name: str, module_path: Path):
        """Imports a module from a path

        This is useful if you need to import a python module to a command
        defined in your local project, unfortunately normal relative `import`
        statements don't work in that context because palm is running in your
        python path, so you need to use this instead.

        Args:
            module_name (str): Name of the module
            module_path (Path): Absolute Path to the module file

        Returns:
            ModuleSpec: The module spec of the imported module,
            or None if the module was not found
        """
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        except ImportError as error:
            click.secho(f'Import error: {error}', fg="red")
            return None
        return mod

    def generate(
        self, template_path: Path, target_path: Path, replacements: dict
    ) -> str:
        return CodeGenerator(template_path, target_path, replacements).run()

    def _build_env_vars(self, env_vars: dict) -> List[str]:
        env_vars_list = []
        for key in env_vars.keys():
            env_vars_list.append(f'-e {key.upper()}={env_vars[key]}')
        return env_vars_list
