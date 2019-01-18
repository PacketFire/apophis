import importlib
from core.readers import fetch_config


class Command:
    def __init__(self, cmd_data):
        self.cmd_data = cmd_data

    def parse_command(self):
        pass


def command_handler(module, handler) -> Command:
    m = importlib.import_module(module)
    cmd = getattr(m, handler)
    return cmd


config = fetch_config()
prefix = config['prefix']

commands = [
    {
        'trigger': 'theo',
        'module': 'cmds.theo',
        'handler': 'TheoCommand'
    },
    {
        'trigger': 'help',
        'module': 'cmds.help',
        'handler': 'HelpCommand'
    },
    {
        'trigger': 'define',
        'module': 'cmds.define',
        'handler': 'DefineCommand'
    },
    {
        'trigger': 'music',
        'module': 'cmds.music',
        'handler': 'MusicCommand'
    }
]
