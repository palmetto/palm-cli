import pytest

# Test defaults - no configuration provided in no_palm_config fixture


def test_has_no_config(no_palm_config):
    assert no_palm_config.has_config is False


def test_image_name_default(no_palm_config):
    assert no_palm_config.image_name == 'test_image_name_default0'


def test_plugins_default(no_palm_config):
    assert no_palm_config.plugins == ['core', 'repo']


# Configuration provided in palm_config fixture


def test_has_config(palm_config):
    assert palm_config.has_config


def test_image_name_config(palm_config):
    assert palm_config.image_name == 'palm-test'


def test_plugins_installed(palm_config):
    assert palm_config.plugins == ['core', 'mock', 'repo']


def test_reads_protected_branches(palm_config):
    assert palm_config.protected_branches == ['main']


def test_raises_on_protected_branches(palm_config_protected):
    with pytest.raises(SystemExit):
        palm_config_protected.validate_branch()
