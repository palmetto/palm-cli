from unittest import mock
from importlib.machinery import ModuleSpec
from palm.plugins.base import BasePlugin


def test_load_plugins_calls_load_plugin(plugin_manager, monkeypatch):
    m = mock.Mock()
    monkeypatch.setattr(plugin_manager, "load_plugin", m)
    plugin_manager.load_plugins(['one', 'two', 'three'])
    m.assert_called()


def test_load_plugin(plugin_manager):
    plugin_manager.load_plugin('test_internal')

    assert plugin_manager.plugins['test_internal']
    assert isinstance(plugin_manager.plugins['test_internal'], BasePlugin)
    assert plugin_manager.is_plugin_command('run')
    assert plugin_manager.plugin_command_dict['run'] == 'test_internal'


def test_extend_command_mapping(plugin_manager, second_test_plugin):
    plugin_manager.plugins['mock_two'] = second_test_plugin
    assert plugin_manager.plugin_command_dict['foo'] == 'mock'

    # Plugin mock_two overrides the command def for 'foo'
    plugin_manager.extend_plugin_command_mapping('mock_two')
    assert plugin_manager.plugin_command_dict['foo'] == 'mock_two'


def test_is_plugin_command(plugin_manager):
    assert plugin_manager.is_plugin_command('foo')
    assert not plugin_manager.is_plugin_command('bar')


def test_command_spec_returns_module_spec(plugin_manager):
    result = plugin_manager.command_spec('foo')

    assert isinstance(result, ModuleSpec)
    assert result.name == 'foo'


def test_plugin_command_list(plugin_manager):
    command_list = plugin_manager.plugin_command_list
    assert len(command_list) == 1
    assert 'foo' in command_list
