from pathlib import Path

import click
from palm.plugins.base import BasePlugin
from palm.docker_details import DockerDetails
from palm.prompts.choice import choice_prompt

class MultiServicePlugin(BasePlugin):
    def __init__(self):
        super().__init__("multi_service", Path(__file__).parent / "commands")
        self.docker_details: DockerDetails = DockerDetails()

    def pick_service(self):
        services = self.docker_details.running_service_names
        selection = choice_prompt(
            "Which container would you like to run this command in?",
            services
        )
        return selection

    def get_full_service_name(self, service: str):
        service = self.docker_details.get_running_service_name(service)
        if not service:
            click.secho(f'Service: {service} not found!', fg='red')
            running_services = '\n'.join(self.docker_details.running_service_names)
            click.echo(f'Running services: \n {running_services}')
