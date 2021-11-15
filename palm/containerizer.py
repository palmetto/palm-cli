from abc import ABC, abstractmethod
from pathlib import Path
import click
from palm.palm_exceptions import AbortPalm
import palm.project_setup_utils as psu


class Containerizer(ABC):
    def __init__(self, ctx, template_dir: Path) -> None:
        self.ctx = ctx
        self.project_name = ctx.obj.palm.image_name
        self.template_dir = template_dir

    @abstractmethod
    def run(self) -> None:
        pass

    def generate(self, target_dir, replacements) -> None:
        self.ctx.obj.generate(self.template_dir, target_dir, replacements)
        psu.make_executable(Path(target_dir, "scripts", "entrypoint.sh"))

    def check_setup(self) -> None:
        if self.has_containerization():
            raise AbortPalm("Containerization already exists")

        if not self.has_env():
            try:
                psu.optionally_create_env()
            except AbortPalm:
                raise AbortPalm("Aborting Containerization")

    def has_containerization(self) -> bool:
        containerization_files = ['docker-compose.yaml', 'Dockerfile']

        for file in containerization_files:
            if Path(file).exists():
                return True

        return False

    def has_env(self) -> bool:
        return psu.has_env()

    @abstractmethod
    def package_manager(self) -> str:
        pass


class PythonContainerizer(Containerizer):
    def run(self) -> None:
        try:
            super().check_setup()
        except AbortPalm as e:
            click.secho(str(e), fg="red")
            return

        package_manager = super().package_manager()

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

        super.generate(target_dir, replacements)

    def package_manager(self) -> str:
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
        use_pip = click.confirm(
            "Unable to detect python package manger, requirements.txt will be used by default. Continue?"
        )
        if use_pip:
            Path("requirements.txt").touch()
        else:
            raise AbortPalm("Aborting")
