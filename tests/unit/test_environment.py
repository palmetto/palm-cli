from os import environ
import pytest
from unittest import mock
import subprocess
from pathlib import Path

import yaml

from palm.code_generator import CodeGenerator


def test_run_in_docker(environment, monkeypatch):
    class MockCompletedProcess:
        returncode = 0
        stdout = b"tested"
        stderr = b""

    monkeypatch.setattr(
        subprocess, "run", lambda *args, **kwargs: MockCompletedProcess()
    )
    success, msg = environment.run_in_docker("test")
    assert success is True
    assert msg == "Success! Palm completed with exit code 0"

def test_exec_in_docker_raises_exception_without_plugin(environment, monkeypatch):
    """
        Environment fixture does not have the multi-service plugin.
        This should raise an exception.
    """
    class MockCompletedProcess:
        returncode = 0
        stdout = b"tested"
        stderr = b""

    monkeypatch.setattr(
        subprocess, "run", lambda *args, **kwargs: MockCompletedProcess()
    )

    with pytest.raises(Exception):
        success, msg = environment.exec_in_docker("test")

def test_exec_in_docker(multi_service_environment, monkeypatch):
    environment = multi_service_environment
    class MockCompletedProcess:
        returncode = 0
        stdout = b"tested"
        stderr = b""

    monkeypatch.setattr(
        subprocess, "run", lambda *args, **kwargs: MockCompletedProcess()
    )
    # Note that service is specified here to prevent the choice prompt
    # from being called.
    success, msg = environment.exec_in_docker("test", service='palm')

    assert success is True
    assert msg == "Success! Palm completed with exit code 0"

def test_run_in_docker_calls_exec_in_docker(multi_service_environment, monkeypatch):
    environment = multi_service_environment
    class MockCompletedProcess:
        returncode = 0
        stdout = b"tested"
        stderr = b""

    monkeypatch.setattr(
        subprocess, "run", lambda *args, **kwargs: MockCompletedProcess()
    )
    m1 = mock.Mock()
    monkeypatch.setattr(environment, "exec_in_docker", m1)
    environment.run_in_docker("test")
    m1.assert_called_once_with("test", env_vars={}, no_bin_bash=False)

def test_import_module(environment):
    module_name = "mock_import"
    module_path = Path(__file__).parent / "mock_import.py"
    result = environment.import_module(module_name, module_path)

    assert hasattr(result, "main")
    assert result.main() is True


def test_generate_calls_code_generator_run(environment, monkeypatch, tmp_path):
    monkeypatch.setattr(CodeGenerator, "run", lambda x: True)

    target_path = tmp_path
    template_path = tmp_path / "templates"
    template_path.mkdir()
    template_config = {}
    with open(template_path / "template-config.yaml", "w") as f:
        f.write(yaml.dump(template_config))

    replacements = {}
    result = environment.generate(template_path, target_path, replacements)
    assert result is True


def test_build_env_vars(environment):
    env_vars = {"palm_env": "test"}
    result = environment._build_env_vars(env_vars)

    assert result == ["-e PALM_ENV=test"]


def test_get_plugin_config_no_config(environment):
    result = environment.plugin_config("mock")
    assert result == None
