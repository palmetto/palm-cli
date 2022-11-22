import pytest
import yaml

from pathlib import Path
from palm.palm_exceptions import InvalidConfigError


@pytest.mark.parametrize("config", [{}])
def test_base_config_init(mock_plugin_config):
    config = mock_plugin_config
    assert config.plugin_name == "test"
    assert config.config_path == Path.cwd() / ".palm" / "config.yaml"


@pytest.mark.parametrize("config", [{"value": "foo"}])
def test_base_config_validation(mock_plugin_config):
    config = mock_plugin_config
    assert config.validate({"value": "test"}) == True

    with pytest.raises(InvalidConfigError):
        config.validate({})


@pytest.mark.parametrize("config", [{}])
def test_base_config_write(mock_plugin_config, tmp_path, monkeypatch):
    config = mock_plugin_config
    config_path = tmp_path / "config.yaml"
    # Set some config to prevent error when writing
    config_path.write_text(yaml.dump({'image_name': 'palm-test'}))
    monkeypatch.setattr(config, "config_path", config_path)
    config._write({"value": "foo"})

    config = yaml.safe_load(config_path.read_text())
    assert config["plugin_config"]["test"]["value"] == "foo"


@pytest.mark.parametrize("config", [{}])
def test_get_config(mock_plugin_config, tmp_path, monkeypatch):
    config = mock_plugin_config
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.dump({'plugin_config': {'test': {'value': 'foo'}}}))
    monkeypatch.setattr(config, "config_path", config_path)

    assert config.get() == {"value": "foo"}
