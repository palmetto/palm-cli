from abc import ABC, abstractmethod
from typing import Dict, Optional
from pathlib import Path
import re
import click
import sys
from palm.palm_exceptions import AbortPalm
import palm.project_setup_utils as psu


class Containerizer(ABC):
    """Abstract base class for containerizer classes

    Containerizer.run() is the main entry point for a containerizer.
    Implementations of run() should call check_setup() and generate()
    """

    def __init__(self, ctx, template_dir: Path) -> None:
        """Containerizer constructor

        Args:
            ctx (click.context): The click context object from the calling command
            template_dir (Path): Path to the templates directory
        """
        self.ctx = ctx
        # By default, image name is read from .palm/config.yaml since this is used
        # to execute commands in the container. This may be overridden in a containerizer
        # but you would need to ensure the image_name matches in config.yaml
        self.project_name = ctx.obj.palm.image_name
        self.template_dir = template_dir

    @abstractmethod
    def run(self) -> None:
        """Entrypoint for containerization

        Must call check_setup() and generate()
        """
        pass

    def generate(self, target_dir: Path, replacements: Dict) -> None:
        """Generate files for containerization

        Args:
            target_dir (Path): Path to directory where generated files should be placed
            replacements (dict): Dict of replacements to be made in template files
        """
        self.ctx.obj.generate(self.template_dir, target_dir, replacements)
        psu.make_executable(Path(target_dir, "scripts", "entrypoint.sh"))

    def check_setup(self) -> None:
        """Check if containerization is possible

        Raises:
            AbortPalm: If the project is already containerized, or has no .env file
        """
        if self.has_containerization():
            raise AbortPalm("Containerization already exists")

        if not self.has_env():
            try:
                psu.optionally_create_env()
            except AbortPalm:
                raise AbortPalm("Aborting Containerization")

    def has_containerization(self) -> bool:
        """Check whether the project has containerization

        Returns:
            bool: true if Dockerfile or docker-compose.yaml exists
        """
        containerization_files = ['docker-compose.yaml', 'Dockerfile']

        for file in containerization_files:
            if Path(file).exists():
                return True

        return False

    def has_env(self) -> bool:
        """Check whether the project has an .env file

        Returns:
            bool: true if .env file exists
        """
        return psu.has_env()


class PythonContainerizer(Containerizer):
    """Containerizer for Python projects"""

    def __init__(
        self, ctx, template_dir: Path, python_version: Optional[str] = '3.8'
    ) -> None:
        """PythonContainerizer constructor

        Args:
            ctx (click.context): The click context object from the calling command
            template_dir (Path): Path to the templates directory
        """
        self.ctx = ctx
        self.project_name = ctx.obj.palm.image_name
        self.template_dir = template_dir
        self.python_version = python_version
        self.package_manager = ''

    def run(self) -> None:
        """Run the containerizer"""
        self.check_setup()
        self.package_manager = self.detect_package_manager()

        super().generate(self.target_dir, self.replacements)

    @property
    def replacements(self) -> Dict:
        """Dict of replacements to be made in template files"""
        return {
            "project_name": self.project_name,
            "package_manager": self.package_manager,
            "python_version": self.python_version,
        }

    @property
    def target_dir(self) -> Path:
        """Get the target directory for containerization

        Returns:
            Path: Path to the target directory
        """
        return Path.cwd()

    def check_setup(self) -> None:
        if not self.validate_python_version():
            click.secho(f"Invalid python version: {self.python_version}", fg="red")
            return

        try:
            super().check_setup()
        except AbortPalm as e:
            click.secho(str(e), fg="red")
            return

    def detect_package_manager(self) -> str:
        """Determine which package manager is in use,
        supports pip3 and poetry, returns "unknown" if neither are found

        Returns:
            str: pip3 | poetry | unknown
        """
        if self.has_requirements_txt():
            return "pip3"
        if self.has_poetry():
            return "poetry"
        # Unknown package manager, prompt to setup requirements.txt
        try:
            self.optionally_add_requirements_txt()
        except AbortPalm:
            click.secho("Aborting containerization", fg="red")
            sys.exit(1)
        return "pip3"

    def has_requirements_txt(self) -> bool:
        """Check for a requirements.txt file in the project root"""
        return Path("requirements.txt").exists()

    def has_poetry(self) -> bool:
        """Check for a poetry.lock file in the project root"""
        return Path("poetry.lock").exists()

    def optionally_add_requirements_txt(self):
        """Optionally, add a requirements.txt file to the project root if it doesn't exist

        Raises:
            AbortPalm: Abort if user does not want to add requirements.txt
        """
        use_pip = click.confirm(
            "Unable to detect python package manger, requirements.txt will be used by default. Continue?"
        )
        if use_pip:
            Path("requirements.txt").touch()
        else:
            raise AbortPalm("Aborting")

    def validate_python_version(self) -> bool:
        """Validate the python version provided by the user

        Args:
            python_version (str): The python version to validate

        Returns:
            bool: True if the python version is valid
        """
        match = re.match(r"^3\.[0-9]{1,2}$", self.python_version)
        return bool(match)
