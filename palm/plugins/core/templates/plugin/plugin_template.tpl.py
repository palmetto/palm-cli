from pathlib import Path
from palm.plugins.base import BasePlugin
import pkg_resources

def get_version():
    try:
        version = pkg_resources.require("palm-{{plugin_name}}")[0].version
    except pkg_resources.DistributionNotFound:
        version = 'unknown'
    return version


{{plugin_class_name}} = BasePlugin(
    name = '{{plugin_name}}', 
    command_dir = Path(__file__).parent / 'commands',
    version = get_version(),
)
