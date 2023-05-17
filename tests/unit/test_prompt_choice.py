import pytest
import click
from unittest import mock

from palm.prompts.choice import choice_prompt

def test_single_choice_is_returned_automatically():
    choices = ['choice1']
    choice = choice_prompt('prompt', choices)
    assert choice == 'choice1'

def test_prompt_contains_choices(monkeypatch):
    choices = ['choice1', 'choice2']

    prompt_mock = mock.Mock(return_value='2')
    monkeypatch.setattr(click, 'prompt', prompt_mock)
    selection = choice_prompt('Test prompt', choices)

    assert 'Test prompt\n1: choice1\n2: choice2\n' in prompt_mock.call_args[0][0]
    assert selection == 'choice2'
