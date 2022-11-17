import shutil
import sys
import zipfile
from pathlib import Path
from unittest import mock

import pygit2
import pytest
import yaml

from palm.environment import Environment
from palm.palm_config import PalmConfig
from palm.plugin_manager import PluginManager
from palm.plugins.base import BasePlugin

sys.modules["palm.plugins.mock"] = mock.Mock()


def test_command():
    return """import click

@click.command('foo')
@click.pass_obj
def cli(environment):
    print('test')
"""


def mock_plugin(name, path):
    plugin_dir = path / name
    commands_dir = plugin_dir / "commands"
    commands_dir.mkdir(parents=True)
    with open(commands_dir / "cmd_foo.py", "w") as f:
        f.write(test_command())

    return BasePlugin(name, commands_dir)


# TODO: parametrize the test_plugin fixture and remove second_test_plugin
@pytest.fixture
def test_plugin(tmp_path):
    return mock_plugin("mock", tmp_path)


@pytest.fixture
def second_test_plugin(tmp_path):
    return mock_plugin("mock_two", tmp_path)


def mock_plugin_manager(tmp_path):
    pm = PluginManager()
    pm.plugins = {"mock": mock_plugin("mock", tmp_path)}
    pm.extend_plugin_command_mapping("mock")

    return pm


@pytest.fixture
def plugin_manager(tmp_path):
    return mock_plugin_manager(tmp_path)


def mock_repository(tmp_path):
    class TemporaryRepository:
        def __init__(self, name, tmp_path):
            self.name = name
            self.tmp_path = tmp_path

        def __enter__(self):
            path = Path(__file__).parent / "data" / self.name
            temp_repo_path = Path(self.tmp_path) / path.stem
            if path.suffix == '.zip':
                with zipfile.ZipFile(path) as zipf:
                    zipf.extractall(self.tmp_path)
            elif path.suffix == ".git":
                shutil.copytree(path, temp_repo_path)
            else:
                raise ValueError(f"Unexpected {path.suffix} extension")

            return temp_repo_path

        def __exit__(self, exc_type, exc_value, traceback):
            pass

    # Note barerepo head is set to test branch
    with TemporaryRepository("barerepo.zip", tmp_path) as path:
        return pygit2.Repository(path)


def write_config_to_path(path, config):
    path.parent.mkdir(parents=True)
    with open(path, "w") as f:
        yaml.dump(config, f)


# TODO: parametrize the palm_config fixture for different configs
@pytest.fixture
def no_palm_config(tmp_path, monkeypatch):
    monkeypatch.setattr(PalmConfig, "_get_repo", lambda self: mock_repository(tmp_path))

    return PalmConfig(Path(tmp_path))


@pytest.fixture
def no_repo_palm_config(tmp_path, monkeypatch):
    monkeypatch.setattr(PalmConfig, '_get_repo', lambda self: None)

    return PalmConfig(Path(tmp_path))


@pytest.fixture
def palm_config(tmp_path, monkeypatch):
    palm_config_path = tmp_path / ".palm" / "config.yaml"
    mock_config = {
        "image_name": "palm-test",
        "plugins": ["mock"],
        "protected_branches": ["main"],
    }
    write_config_to_path(palm_config_path, mock_config)
    monkeypatch.setattr(PalmConfig, "_get_repo", lambda self: mock_repository(tmp_path))
    return PalmConfig(Path(tmp_path))


@pytest.fixture
def palm_config_protected(tmp_path, monkeypatch):
    palm_config_path = tmp_path / ".palm" / "config.yaml"
    mock_config = {"image_name": "", "plugins": [], "protected_branches": ["main"]}
    write_config_to_path(palm_config_path, mock_config)

    def mock_current_branch(self):
        return "main"

    monkeypatch.setattr(PalmConfig, "_get_repo", lambda self: mock_repository(tmp_path))
    monkeypatch.setattr(PalmConfig, "_get_current_branch", mock_current_branch)
    return PalmConfig(Path(tmp_path))


@pytest.fixture
def environment(tmp_path, monkeypatch):
    monkeypatch.setattr(PalmConfig, "_get_repo", lambda self: mock_repository(tmp_path))
    pm = mock_plugin_manager(tmp_path)
    config = PalmConfig(Path(tmp_path))
    return Environment(pm, config)
