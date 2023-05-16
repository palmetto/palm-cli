import click
from typing import List
from collections import OrderedDict

def choice_prompt(prompt: str, options: List[str]) -> str:
    """Prompt the user to select from a list of options

    Args:
        prompt (str): The prompt text to display to the user before the options
        options (List[str]): The list of options to choose from

    Returns:
        str: The option the user selected
    """
    if len(options) == 1:
        return options[0]

    choice_map = OrderedDict((f'{i}', option) for i, option in enumerate(options, 1))
    choices = choice_map.keys()
    choice_lines = [f'{k}: {v}' for k, v in choice_map.items()]
    default = 1

    prompt = '\n'.join([
        prompt,
        '\n'.join(choice_lines),
        f'Select from {len(choices)} options above',
    ])

    selection = click.prompt(
        prompt,
        type=click.Choice(choices),
        show_choices=False,
        default=default
    )

    return choice_map[selection]
