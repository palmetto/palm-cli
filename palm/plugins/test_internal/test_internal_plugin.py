from pathlib import Path
from palm.plugins.base import BasePlugin

# This plugin is intended for use in testing palm-cli.
# It is not intended to be used in production.

TestInternalPlugin = BasePlugin(
    name='test_internal',
    command_dir=Path(__file__).parent / 'commands',
)
