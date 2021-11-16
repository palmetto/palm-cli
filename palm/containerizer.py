from abc import ABC, abstractmethod
from pathlib import Path
import click
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
        pass

    def generate(self, target_dir: Path, replacements: dict) -> None:
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

    @abstractmethod
    def package_manager(self) -> str:
        """Check for the package manager used by the project
        this will be used to determine the correct logic in entrypoint.sh

        Returns:
            str: Name of package manager
        """        
        pass


class PythonContainerizer(Containerizer):
    """Containerizer for Python projects"""

    def run(self) -> None:
        """Run the containerizer"""
        try:
            super().check_setup()
        except AbortPalm as e:
            click.secho(str(e), fg="red")
            return

        package_manager = self.package_manager()

        if package_manager == "unknown":
            try:
                self.optionally_add_requirements_txt()
            except AbortPalm:
                click.secho("Aborting containerization", fg="red")
                return
            package_manager = "pip3"

        target_dir = Path.cwd()
        replacements = {
            "project_name": self.project_name,
            "package_manager": package_manager,
        }

        super().generate(target_dir, replacements)

    def package_manager(self) -> str:
        """Determine which package manager is in use,
        supports pip3 and poetry, returns "unknown" if neither are found

        Returns:
            str: pip3 | poetry | unknown
        """        
        if self.has_requirements_txt():
            return "pip3"
        if self.has_poetry():
            return "poetry"

        return "unknown"

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
