import pytest
import os
import yaml
from pathlib import Path
from click.testing import CliRunner
from palm.cli import cli


@pytest.fixture
def use_palm_dir():
    """Palm runner with a .palm directory"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir('.palm')

        yield runner


@pytest.fixture
def use_empty_dir():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner


def test_cli_has_core_and_repo_plugins_by_default():
    """Test no-op run command"""
    plugins = cli.plugin_manager.plugins
    assert list(plugins.keys()) == ['core', 'repo']


def test_run_command():
    """Test no-op run command"""
    cli.plugin_manager.load_plugin('test_internal')
    result = CliRunner().invoke(cli, ["run"])
    assert result.exit_code == 0
    assert "completed" in result.output


# Command detection from .palm/ in cwd


@pytest.mark.skip(reason="Loading commands from .palm not currently working in test")
def test_command_from_palm_dir(use_palm_dir):
    runner = use_palm_dir
    result = runner.invoke(cli, ["test"])
    assert Path('.palm', 'cmd_test.py').exists()
    assert result.exit_code == 0
    assert "test command running!" in result.output


# Palm Init tests


def test_palm_init(use_empty_dir):
    runner = use_empty_dir
    result = runner.invoke(cli, ["init", "--commands", "run", "-c", "test"])
    assert result.exit_code == 0
    assert "Success! Project initialized with Palm CLI" in result.output
    assert Path('.palm').exists()
    assert Path('.palm').is_dir()
    assert "Adding template for run" in result.output
    assert "Adding template for test" in result.output
    assert Path('.palm', 'cmd_run.py').exists()
    assert Path('.palm', 'cmd_test.py').exists()


# Palm Scaffold tests


def test_scaffold_new_command(use_palm_dir):
    runner = use_palm_dir
    result = runner.invoke(cli, ["scaffold", "command", "--name", "test"])
    assert result.exit_code == 0
    assert "test command created in" in result.output
    target_path = Path('.palm', 'cmd_test.py')
    assert target_path.exists()
    assert "@click.command('test')" in target_path.read_text()


def test_scaffold_new_command_group(use_palm_dir):
    runner = use_palm_dir
    result = runner.invoke(
        cli, ["scaffold", "group", "--group", "groupname", "--command", "test"]
    )
    assert result.exit_code == 0
    assert f"groupname command group created in" in result.output
    target_path = Path('.palm', 'cmd_groupname.py')
    assert target_path.exists()
    assert "@click.group()" in target_path.read_text()
    assert "def test(environment):" in target_path.read_text()


def test_scaffold_config(use_palm_dir):
    runner = use_palm_dir
    result = runner.invoke(
        cli,
        [
            "scaffold",
            "config",
            "--image-name",
            "testing",
            "--plugins",
            "test",
            "-p",
            "test-two",
            "--protected-branches",
            "master",
            "-pb",
            "main",
        ],
    )
    config_path = Path('.palm', 'config.yaml')
    assert result.exit_code == 0
    assert f"Palm config created!" in result.output
    assert config_path.exists()
    config = yaml.safe_load(config_path.read_text())
    assert config['image_name'] == 'testing'
    assert config['plugins'] == ['test', 'test-two']
    assert config['protected_branches'] == ['master', 'main']
