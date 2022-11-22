import pytest
import yaml

# Test defaults - no configuration provided in no_palm_config fixture


def test_image_name_default(no_palm_config):
    assert no_palm_config.image_name == 'test_image_name_default0'


def test_plugins_default(no_palm_config):
    assert no_palm_config.plugins == ['core', 'repo']


# Configuration provided in palm_config fixture


def test_has_config(palm_config):
    assert len(palm_config.config.keys()) > 0


def test_image_name_config(palm_config):
    assert palm_config.image_name == 'palm-test'


def test_plugins_installed(palm_config):
    assert palm_config.plugins == ['core', 'mock', 'repo']


def test_reads_protected_branches(palm_config):
    assert palm_config.protected_branches == ['main']


def test_raises_on_protected_branches(palm_config_protected):
    with pytest.raises(SystemExit):
        palm_config_protected.validate_branch()


# Global config


def test_create_global_config_file(no_palm_config, tmp_path):
    config_path = tmp_path / '.palm' / 'config.yaml'
    no_palm_config._create_global_config_file(config_path)

    assert config_path.exists()
    global_config = yaml.load(config_path.read_text())
    assert global_config.keys() == {'plugins', 'excluded_commands'}


def test_get_global_config(no_palm_config, tmp_path):
    config_path = tmp_path / '.palm' / 'config.yaml'
    no_palm_config._create_global_config_file(config_path)
    test_config = {'plugins': ['foo'], 'excluded_commands': ['bar']}
    config_path.write_text(yaml.dump(test_config))

    result = no_palm_config._get_global_config(config_path)
    assert result == test_config


def test_get_config_merges_repo_and_global(no_palm_config, monkeypatch):
    repo_config = {'plugins': ['foo'], 'excluded_commands': ['bar']}
    global_config = {'plugins': ['baz'], 'excluded_commands': ['qux']}
    monkeypatch.setattr(no_palm_config, '_get_repo_config', lambda: repo_config)
    monkeypatch.setattr(no_palm_config, '_get_global_config', lambda: global_config)

    result = no_palm_config._get_config()
    assert result == {'plugins': ['baz', 'foo'], 'excluded_commands': ['qux', 'bar']}
