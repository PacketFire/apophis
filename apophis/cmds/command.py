import importlib


class Command:
    def handle(self):
        pass


def command_handler(module, handler) -> Command:
    m = importlib.import_module(module)
    cmd = getattr(m, handler)
    return cmd


async def check_permissions(context, user) -> bool:
    statement = '''
    select level from permissions where username = $1;
    '''
    rows = await context['db'].fetch(statement, str(user))

    if rows[0]['level'] >= 1:
        return True
    else:
        return False


commands = [
    {
        'trigger': 'theo',
        'module': 'cmds.theo',
        'handler': 'TheoCommand',
        'permissions': 0
    },
    {
        'trigger': 'help',
        'module': 'cmds.help',
        'handler': 'HelpCommand',
        'permissions': 0
    },
    {
        'trigger': 'define',
        'module': 'cmds.define',
        'handler': 'DefineCommand',
        'permissions': 0
    },
    {
        'trigger': 'music',
        'module': 'cmds.music',
        'handler': 'MusicCommand',
        'permissions': 1
    },
    {
        'trigger': 'access',
        'module': 'cmds.access',
        'handler': 'AccessCommand',
        'permissions': 2
    }
]
