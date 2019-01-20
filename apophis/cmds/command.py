import importlib


class Command:
    def handle(self):
        pass


def command_handler(module, handler) -> Command:
    m = importlib.import_module(module)
    cmd = getattr(m, handler)
    return cmd


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
