import os
from pathlib import Path

import pytest

from palm.containerizer import PythonContainerizer


class MockContext:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# Clear abstract methods to allow testing ABC
PythonContainerizer.__abstractmethods__ = set()


def test_detect_package_manager(tmp_path, environment):
    os.chdir(tmp_path)
    ctx = MockContext(obj=environment)
    pc = PythonContainerizer(ctx.obj, tmp_path)

    with pytest.raises(Exception):
        pc.detect_package_manager()

    Path("poetry.lock").touch()
    assert pc.detect_package_manager() == "poetry"
    Path("requirements.txt").touch()
    assert pc.detect_package_manager() == "pip3"


def test_has_requirements_txt(tmp_path, environment):
    os.chdir(tmp_path)
    ctx = MockContext(obj=environment)
    c = PythonContainerizer(ctx.obj, tmp_path)

    assert not c.has_requirements_txt()
    Path("requirements.txt").touch()
    assert c.has_requirements_txt()


def test_has_poetry(tmp_path, environment):
    os.chdir(tmp_path)
    ctx = MockContext(obj=environment)
    c = PythonContainerizer(ctx.obj, tmp_path)

    assert not c.has_poetry()
    Path("poetry.lock").touch()
    assert c.has_poetry()


def test_run(tmp_path, environment):
    templates_dir = (
        Path(__file__).parents[2] / "palm/plugins/core/templates/containerize"
    )

    os.chdir(tmp_path)
    Path(".env").touch()
    Path("requirements.txt").touch()
    ctx = MockContext(obj=environment)
    c = PythonContainerizer(ctx.obj, templates_dir)
    c.run()

    assert Path(tmp_path, "Dockerfile").exists()
    assert Path(tmp_path, "docker-compose.yaml").exists()
    assert Path(tmp_path, "scripts/entrypoint.sh").exists()


def test_validate_python_version(tmp_path, environment):
    ctx = MockContext(obj=environment)
    default_version_pc = PythonContainerizer(ctx.obj, tmp_path)
    assert default_version_pc.validate_python_version()
    valid_version_pc = PythonContainerizer(ctx.obj, tmp_path, '3.9')
    assert valid_version_pc.validate_python_version()

    invalid_version_pc = PythonContainerizer(ctx.obj, tmp_path, '2.8')
    assert not invalid_version_pc.validate_python_version()
    invalid_value_pc = PythonContainerizer(ctx.obj, tmp_path, 'foo')
    assert not invalid_value_pc.validate_python_version()
