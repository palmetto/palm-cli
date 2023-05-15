import shlex
import yaml
import subprocess
from pathlib import Path

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
    def service_names(self):
        services = list(self.config.get('services', {}).keys())
        service_names = []
        for service in services:
            service_config = self.config.get('services', {}).get(service, {})
            if service_config.get('container_name'):
                service_names.append(service_config.get('container_name'))
            else:
                name = self._get_docker_service_name(service)
                # Only append names of running services
                if name:
                    service_names.append(name)
        return service_names

    def _get_docker_service_name(self, service):
        cmd = 'docker ps -a --filter name={service} --format {{{{.Names}}}}'.format(service=service)
        result = subprocess.run(
          shlex.split(cmd),
          check=True,
          capture_output=True
        )
        if result.returncode != 0:
            raise Exception(result.stderr)
        return result.stdout.decode('utf-8').strip()
