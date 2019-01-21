import importlib


class Command:
    def handle(self):
        pass


def command_handler(module, handler) -> Command:
    m = importlib.import_module(module)
    cmd = getattr(m, handler)
    return cmd


async def check_permissions(user, context) -> int:
    statement = '''
    select level from permissions where username = $1;
    '''
    rows = await context['db'].fetch(statement, user)
    return int(rows[0]['level'])


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
    },
    {
        'trigger': 'access',
        'module': 'cmds.access',
        'handler': 'AccessCommand'
    }
]
