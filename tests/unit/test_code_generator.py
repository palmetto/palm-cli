import yaml

from palm.code_generator import CodeGenerator


def setup_templates(path):
    template_path = path / "templates"
    template_path.mkdir(parents=True)

    with open(template_path / "template.py", "w") as f:
        f.write(
            """def foo():
            print(f'Hello {{name}}')
        """
        )

    template_config = {
        "directories": ["{{dirname}}"],
        "files": [{"template.py": "{{dirname}}/generated_{{filename}}.py"}],
    }
    with open(template_path / "template-config.yaml", "w") as f:
        yaml.dump(template_config, f)

    target_path = path / "target"
    target_path.mkdir(parents=True)

    return template_path, target_path


def test_get_config(tmp_path):
    template_path, target_path = setup_templates(tmp_path)
    codegen = CodeGenerator(template_path, target_path, {})
    config = codegen.get_config()

    assert config["directories"] == ["{{dirname}}"]
    assert type(config["files"]) == list
    assert config["files"][0] == {
        "template.py": "{{dirname}}/generated_{{filename}}.py"
    }


def test_run_generator(tmp_path):
    template_path, target_path = setup_templates(tmp_path)
    replacements = {"name": "Murphy Moulds", "dirname": "da_team", "filename": "murphy"}
    codegen = CodeGenerator(template_path, target_path, replacements)
    result = codegen.run()
    expected_file = target_path / "da_team" / "generated_murphy.py"

    assert result == "Generated successfully"
    assert expected_file.exists()

    file_contents = expected_file.read_text()
    assert file_contents.startswith("def foo():")
    assert "print(f'Hello Murphy Moulds')" in file_contents
