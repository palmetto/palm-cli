import os
from pathlib import Path

from palm.containerizer import Containerizer


class MockContext:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# Clear abstract methods to allow testing ABC
Containerizer.__abstractmethods__ = set()


def test_project_name_matches_palm_config_image_name(tmp_path, environment):
    ctx = MockContext(obj=environment)
    c = Containerizer(ctx, tmp_path)

    assert c.project_name == "test_project_name_matches_palm0"


def test_check_has_containerization(tmp_path, environment):
    os.chdir(tmp_path)
    ctx = MockContext(obj=environment)
    result = Containerizer(ctx, tmp_path).has_containerization()

    assert result == False
    Path("Dockerfile").touch()
    result = Containerizer(ctx, tmp_path).has_containerization()
    assert result


def test_has_env(tmp_path, environment):
    os.chdir(tmp_path)
    ctx = MockContext(obj=environment)
    result = Containerizer(ctx, tmp_path).has_env()
    assert result == False

    Path(".env").touch()
    result = Containerizer(ctx, tmp_path).has_env()
    assert result


def test_generate(tmp_path, environment):
    templates_dir = (
        Path(__file__).parents[2] / "palm/plugins/core/templates/containerize"
    )
    ctx = MockContext(obj=environment)
    c = Containerizer(ctx, templates_dir)
    c.generate(tmp_path, {})

    assert Path(tmp_path, "Dockerfile").exists()
    assert Path(tmp_path, "docker-compose.yaml").exists()
    assert Path(tmp_path, "scripts/entrypoint.sh").exists()


def test_generated_entrypoint_is_executable(tmp_path, environment):
    templates_dir = (
        Path(__file__).parents[2] / "palm/plugins/core/templates/containerize"
    )
    ctx = MockContext(obj=environment)
    c = Containerizer(ctx, templates_dir)
    c.generate(tmp_path, {})

    entrypoint = Path(tmp_path, "scripts/entrypoint.sh")
    assert os.access(entrypoint, os.X_OK)
