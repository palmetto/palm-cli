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
    def service_names(self) -> list[str]:
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
        cmd = 'docker ps -a --filter name={service} --format {{{{.Names}}}}'.format(service=service)
        result = subprocess.run(
          shlex.split(cmd),
          check=True,
          capture_output=True
        )
        if result.returncode != 0:
            return False

        return True
