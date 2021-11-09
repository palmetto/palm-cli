from pathlib import Path
from palm.plugins.base import BasePlugin
import palm.plugins.core as core_plugin


def test_plugin_defined():
    assert core_plugin.Plugin is not None


def test_plugin_is_instance_of_base_plugin():
    assert isinstance(core_plugin.Plugin, BasePlugin)


def test_plugin_name_is_core():
    assert core_plugin.Plugin.name == 'core'


def test_core_plugin_command_dir():
    cmd_dir = core_plugin.Plugin.command_dir
    assert isinstance(cmd_dir, Path)
    assert cmd_dir.exists()
    assert cmd_dir.is_dir()
    assert cmd_dir.name == 'commands'


def test_core_plugin_commands():
    cmds = core_plugin.Plugin.all_commands()
    assert isinstance(cmds, list)
    assert len(cmds) > 0
    assert 'build' in cmds
    assert 'plugin' in cmds
    assert 'scaffold' in cmds
    assert 'update' in cmds


def test_core_plugin_command_map():
    cmd_map = core_plugin.Plugin.command_map()
    assert isinstance(cmd_map, dict)
    assert len(cmd_map.values()) > 0
    for val in cmd_map.values():
        assert val == 'core'
