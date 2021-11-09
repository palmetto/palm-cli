from pathlib import Path
from palm.plugins.base import BasePlugin
import palm.plugins.repo as repo_plugin


def test_plugin_defined():
    assert repo_plugin.Plugin is not None


def test_plugin_is_instance_of_base_plugin():
    assert isinstance(repo_plugin.Plugin, BasePlugin)


def test_plugin_name_is_core():
    assert repo_plugin.Plugin.name == 'repo'


def test_repo_plugin_command_dir():
    cmd_dir = repo_plugin.Plugin.command_dir
    assert isinstance(cmd_dir, Path)
    assert cmd_dir.exists()
    assert cmd_dir.is_dir()
    assert cmd_dir.name == '.palm'
