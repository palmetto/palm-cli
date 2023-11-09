import importlib
from pathlib import Path
from typing import List, Optional, Tuple

import click
from palm.plugins.base import BasePlugin
from pydantic import BaseModel

from palm.plugin_manager import PluginManager
from palm.utils import run_on_host, run_in_docker

from .code_generator import CodeGenerator
from .palm_config import PalmConfig
from .prompts.choice import choice_prompt as choice_prompt_func


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
        silent: Optional[bool] = False,
    ) -> Tuple[bool, str]:
        env_vars_list = self._build_env_vars(env_vars)

        if self.palm.is_multi_service:
            self.exec_in_docker(cmd, env_vars=env_vars, no_bin_bash=no_bin_bash)
            return

        return run_in_docker(
            cmd, self.palm.image_name, env_vars_list, no_bin_bash, silent
        )

    def exec_in_docker(
        self,
        cmd: str,
        env_vars: Optional[dict] = {},
        no_bin_bash: Optional[bool] = False,
        service: Optional[str] = None,
    ) -> Tuple[bool, str]:
        if not self.palm.is_multi_service:
            click.secho(
                "This command is only available in multi-service repos", fg="red"
            )
            raise Exception("exec_in_docker only available in multi-service repos")

        multi_service_plugin = self.get_plugin("multi_service")
        if not service:
            service = multi_service_plugin.pick_service()

        click.secho(f"Executing command `{cmd}` in {service}...", fg="yellow")

        docker_cmd = ["docker compose exec -it"]
        docker_cmd.extend(self._build_env_vars(env_vars))
        docker_cmd.append(service)
        if not no_bin_bash:
            docker_cmd.append(f'/bin/bash -c')
        docker_cmd.append(f'"{cmd}"')

        ex_code, _, _ = run_on_host(" ".join(docker_cmd), check=True)

        if ex_code == 0:
            return (True, "Success! Palm completed with exit code 0")
        return (False, f"Fail! Palm exited with code {ex_code}")

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
            click.secho(f"Import error: {error}", fg="red")
            return None
        return mod

    def generate(
        self, template_path: Path, target_path: Path, replacements: dict
    ) -> str:
        """Runs a template through the code generator

        Args:
            template_path (Path): Path to the directory containing the template
            target_path (Path): Path to the directory where the generated code will be written
            replacements (dict): Dict of replacements to make in the template

        Returns:
            str: The path to the generated code
        """
        return CodeGenerator(template_path, target_path, replacements).run()

    def _build_env_vars(self, env_vars: dict) -> List[str]:
        env_vars_list = []
        for key in env_vars.keys():
            env_vars_list.append(f"-e {key.upper()}={env_vars[key]}")
        return env_vars_list

    def plugin_config(self, plugin_name: str) -> Optional[BaseModel]:
        """Returns the config for a plugin

        Args:
            plugin_name (str): The name of the plugin

        Returns:
            Optional[BaseModel]: The config for the plugin, or None if the plugin
            is not found or does not have a config
        """
        plugin = self.get_plugin(plugin_name)
        if plugin and plugin.config:
            return plugin.config.get()
        return None

    def get_plugin(self, plugin_name: str) -> BasePlugin:
        """Returns a plugin by name

        Args:
            plugin_name (str): The name of the plugin

        Returns:
            BasePlugin: The plugin
        """
        try:
            plugin = self.plugin_manager.plugins.get(plugin_name)
        except KeyError:
            click.secho(f"Plugin {plugin_name} not found", fg="red")
            return None

        return plugin

    def choice_prompt(self, prompt: str, options: List[str]) -> str:
        return choice_prompt_func(prompt, options)
