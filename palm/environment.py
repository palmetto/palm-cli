import importlib
from pathlib import Path
from typing import List, Optional, Tuple

import click
from pydantic import BaseModel

from palm.plugin_manager import PluginManager
from palm.utils import run_on_host, run_in_docker

from .code_generator import CodeGenerator
from .palm_config import PalmConfig


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
        return run_in_docker(
            cmd,
            self.palm.image_name,
            self.palm.is_multi_service,
            env_vars_list,
            no_bin_bash,
            silent
        )

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
        plugin = self.plugin_manager.plugins.get(plugin_name)
        if plugin and plugin.config:
            return plugin.config.get()
        return None
