import pytest
from unittest import mock
from click import HelpFormatter
from palm.cli import PalmCLI


@pytest.fixture
def mock_help_formatter(monkeypatch):
    formatter = HelpFormatter()
    return formatter


class MockCommand:
    def __init__(self, name):
        self.name = name

    @property
    def hidden(self):
        return False

    def get_short_help_str(self, limit):
        return self.name


def test_format_commands_adds_headings_for_plugins(mock_help_formatter, monkeypatch):
    """Test command formatting"""
    PalmCLIInstance = PalmCLI()
    monkeypatch.setattr(PalmCLIInstance, 'list_commands', lambda x: ['test'])
    m = mock.Mock()
    monkeypatch.setattr(mock_help_formatter, "write_heading", m)
    ctx = {}
    PalmCLIInstance.format_commands(ctx, mock_help_formatter)
    # Test command exists in the core plugin
    m.assert_called_once_with('Core')


def test_format_commands_properly_outputs_command_help(
    mock_help_formatter, monkeypatch
):
    """Test command formatting"""
    PalmCLIInstance = PalmCLI()
    monkeypatch.setattr(PalmCLIInstance, 'list_commands', lambda x: ['test'])
    m = mock.Mock()
    monkeypatch.setattr(mock_help_formatter, "write_dl", m)
    ctx = {}
    PalmCLIInstance.format_commands(ctx, mock_help_formatter)
    m.assert_called()
    expected_command_dl = ('test', 'Run tests for your application (pytest)')
    m.assert_called_with([expected_command_dl])


def test_format_commands_handles_multiple_groups(mock_help_formatter, monkeypatch):
    PalmCLIInstance = PalmCLI()

    monkeypatch.setattr(PalmCLIInstance, 'list_commands', lambda x: ['test', 'foo'])
    monkeypatch.setattr(
        PalmCLIInstance, 'get_command', lambda ctx, cmd_name: MockCommand(cmd_name)
    )
    plugin_manager = PalmCLIInstance.plugin_manager
    mock_plugin_dict = {
        'test': 'core',
        'foo': 'bar',
    }
    monkeypatch.setattr(plugin_manager, 'plugin_command_dict', mock_plugin_dict)

    m = mock.Mock()
    monkeypatch.setattr(mock_help_formatter, "write_heading", m)
    ctx = {}
    PalmCLIInstance.format_commands(ctx, mock_help_formatter)

    assert m.call_count == 2
    # This is dumb and gross, but properly asserting multiple call args in python 3.7
    # doesn't seem to work.
    call_args = [str(call) for call in m.call_args_list]
    assert "call('Core')" in call_args
    assert "call('Bar')" in call_args
