import yaml
import click

from typing import Optional, List
from pathlib import Path
from pydantic import BaseModel
from palm.plugins.base_plugin_config import BasePluginConfig


class MultiServicePluginConfigModel(BaseModel):
    services: Optional[List[str]]


class MultiServicePluginConfig(BasePluginConfig):
    def __init__(self):
        super().__init__('multi_service', MultiServicePluginConfigModel)

    def set(self) -> dict:
        config = {}
        docker_compose_path = Path.cwd() / "docker-compose.yaml"
        if not docker_compose_path.exists():
            click.secho(
                f"docker-compose.yaml not found at {docker_compose_path}", fg="red"
            )
            return {}

        docker_compose = yaml.safe_load(docker_compose_path.read_text())

        services = list(docker_compose.get('services', {}).keys())
        config['services'] = services

        return config
