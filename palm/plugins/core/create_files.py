from pathlib import Path
from typing import List, Optional
import yaml


def create_config(
    palm_dir,
    image_name,
    plugins: Optional[List] = [],
    protected_branches: Optional[List] = [],
):
    config_path = f'{palm_dir}/config.yaml'
    base_config = {
        'image_name': image_name,
        'plugins': plugins,
        'protected_branches': protected_branches,
    }

    with open(config_path, 'w') as file:
        yaml.safe_dump(base_config, file)


def create_command(ctx, command: str, template_dir: Path, target_dir: Path):
    """Creates a new cmd file from template"""

    replacements = {
        'command': command,
    }

    ctx.obj.generate(template_dir, target_dir, replacements)
