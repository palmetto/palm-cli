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
