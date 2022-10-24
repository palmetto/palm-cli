from pathlib import Path

import yaml

path_suffix = "palm/plugins/core/templates/plugin/"
plugin_dir = Path.cwd() / path_suffix


def test_defined_template_files_exist():
    """Simple but a place bugs hide"""
    plugin_conf = yaml.safe_load((plugin_dir / "template-config.yaml").read_text())
    for filename in [list(f.keys())[0] for f in plugin_conf["files"]]:
        assert (plugin_dir / filename).exists()
