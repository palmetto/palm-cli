from pathlib import Path

import yaml

from palm.plugins.core.create_files import *


class MockContext:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_create_config(tmp_path):
    create_config(tmp_path, "test-image", ["test"], ["main"])
    result = yaml.safe_load(Path(tmp_path, "config.yaml").read_text())

    assert result["image_name"] == "test-image"
    assert result["plugins"] == ["test"]
    assert result["protected_branches"] == ["main"]


def test_create_command(tmp_path, environment):
    target_dir = Path(tmp_path / "target")
    target_dir.mkdir()
    template_dir = Path(tmp_path / "templates")
    template_dir.mkdir()
    with open(template_dir / "new_cmd.tpl.py", "a") as f:
        f.write("{{command}}")
    template_config = {"files": [{"new_cmd.tpl.py": "cmd_{{command}}.py"}]}
    with open(template_dir / "template-config.yaml", "a") as f:
        f.write(yaml.dump(template_config))

    ctx = MockContext(obj=environment)

    create_command(ctx.obj, "testing", template_dir, target_dir)

    cmd_file = Path(target_dir / "cmd_testing.py")
    assert cmd_file.exists()

    contents = cmd_file.read_text()
    assert "testing" == contents
