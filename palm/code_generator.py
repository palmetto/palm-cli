from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import yaml


class CodeGenerator:
    def __init__(
        self, template_path: Path, target_path: Path, replacements: dict
    ) -> None:
        """Palm core code generator class

        Args:
            template_path (Path): Path to the directory containing your templates and template-config.yaml
            target_path (Path): Path to directory where generated files will be written
            replacements (dict): Dictionary of templated strings to replace
        """
        self.template_path = template_path
        self.target_path = target_path
        self.replacements = replacements
        self.config = self.get_config()

    def run(self) -> str:
        """Runs code generator

        Using the config from template_path/template-config.yaml
        Generate all directories then generate all files with jinja templating.

        Returns:
            str: Result message
        """
        env = Environment(
            loader=FileSystemLoader(self.template_path),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        for directory in self.config.get("directories", []):
            directory_path = Path(
                Path.cwd(),
                self.target_path,
                env.from_string(directory).render(self.replacements),
            )

            if not directory_path.is_dir():
                directory_path.mkdir(parents=True)
            else:
                print(f"{directory_path} already exists")

        for file_item in self.config.get("files", []):
            for key in file_item:
                template = key
                destination = env.from_string(file_item[key]).render(self.replacements)
                print(f'Generating {template} to {destination}')
                t = env.get_template(template)
                templated_contents = t.render(self.replacements)

                with open(Path(Path.cwd(), self.target_path, destination), 'w') as fh:
                    fh.write(templated_contents)

        return "Generated successfully"

    def get_config(self) -> dict:
        """Read configuration from template_path/template-config.yaml

        Example template-config.yaml:
            directories:
            - "foo"
            - "foo/{{some_replacement}}"

            files:
            - template_name.py: "path/to/destination.ext"
            - main.py: "foo/{{some_replacement}}/__main__.py"


        Returns:
            dict: dict representation of template-config.yaml
        """
        config_data = {}

        try:
            config_data = yaml.safe_load(
                (self.template_path / "template-config.yaml").read_text()
            )
        except FileNotFoundError:
            print(f"No template-config.yaml found in {self.template_path}")
        except:
            raise Exception("Error reading template-config.yaml")
        return config_data
