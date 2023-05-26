import shlex
import yaml
import subprocess
from typing import List
from pathlib import Path

from .palm_exceptions import NoRunningServicesError


class DockerDetails:
    """Provides details about the docker environment to the palm config
    which can be used by commands and plugins that need to interact with
    docker services or containers.
    """

    def __init__(self):
        self.path = self.find_docker_compose_file()
        self.config = self.read()

    def find_docker_compose_file(self) -> Path:
        """Finds the docker-compose.yml file in the current working directory
        or raises an exception if it does not exist.

        Returns:
            Path: The path to the docker-compose.yml file
        """
        extensions = ["yml", "yaml"]
        for ext in extensions:
            path = Path.cwd() / f"docker-compose.{ext}"
            if path.exists():
                return path
        raise FileNotFoundError("No docker-compose.yml or docker-compose.yaml file found")

    def read(self):
        return yaml.safe_load(self.path.read_text())

    @property
    def service_names(self) -> List[str]:
        """Gets the names of currently running services for the current project.

        Returns:
            list[str]: The names of the running services
        """
        services = list(self.config.get('services', {}).keys())
        running_services = [s for s in services if self.check_service_is_running(s)]

        if not running_services:
            raise NoRunningServicesError()
        return services

    def check_service_is_running(self, service: str) -> bool:
        """Check if a service is running in Docker

        Args:
            service (str): The service name defined in the docker-compose.yml

        Returns:
            str: The name of the running service
        """
        cmd = 'docker ps -a --filter name={service} --format {{{{.Names}}}}'.format(
            service=service
        )
        result = subprocess.run(shlex.split(cmd), check=True, capture_output=True)
        if result.returncode != 0:
            return False

        return True
