import os
from pathlib import Path

import click

import palm.project_setup_utils as project_setup_utils


def test_has_env(tmp_path):
    os.chdir(tmp_path)
    assert not project_setup_utils.has_env()

    Path(".env").touch()
    assert project_setup_utils.has_env()


def test_optionally_create_env(tmp_path, monkeypatch):
    monkeypatch.setattr(click, "confirm", lambda x: True)
    os.chdir(tmp_path)
    project_setup_utils.optionally_create_env()
    assert Path(".env").exists()


def test_make_executable(tmp_path):
    os.chdir(tmp_path)
    Path("file.sh").touch()
    project_setup_utils.make_executable("file.sh")
    assert os.access("file.sh", os.X_OK)
