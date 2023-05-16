import shlex
import yaml
import subprocess
from pathlib import Path

from .palm_exceptions import NoRunningServicesError

class DockerDetails:
    """Provides details about the docker environment to the palm config
    which can be used by commands and plugins that need to interact with
    docker services or containers.
    """
    def __init__(self):
        self.path = Path.cwd() / "docker-compose.yml"
        self.config = self.read()

    def read(self):
        return yaml.safe_load(self.path.read_text())

    @property
    def running_service_names(self) -> list[str]:
        """Gets the names of currently running services for the current project.

        Returns:
            list[str]: The names of the running services
        """
        services = list(self.config.get('services', {}).keys())
        service_names = []
        for service in services:
            name = self.get_running_service_name(service)
            # Only append names of running services
            if name:
                service_names.append(name)
        if not service_names:
            raise NoRunningServicesError()
        return service_names

    def get_running_service_name(self, service: str) -> str:
        """Gets the name of a running service based on the service name
        defined in the docker-compose.yml file.

        Args:
            service (str): The service name defined in the docker-compose.yml

        Returns:
            str: The name of the running service
        """
        cmd = 'docker ps -a --filter name={service} --format {{{{.Names}}}}'.format(service=service)
        result = subprocess.run(
          shlex.split(cmd),
          check=True,
          capture_output=True
        )
        if result.returncode != 0:
            raise Exception(result.stderr)
        return result.stdout.decode('utf-8').strip()

    @property
    def is_multi_service(self) -> bool:
        """Checks if the docker-compose.yml has more than one service defined"""
        return len(self.config.get('services', {})) > 1
