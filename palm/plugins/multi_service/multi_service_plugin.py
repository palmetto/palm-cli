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
        services = self.docker_details.service_names
        selection = choice_prompt(
            "Which container would you like to run this command in?", services
        )
        return selection
