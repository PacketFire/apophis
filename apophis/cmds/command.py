import importlib


class Command:
    def handle(self):
        pass


def command_handler(module, handler) -> Command:
    m = importlib.import_module(module)
    cmd = getattr(m, handler)
    return cmd


async def get_permissions(context, user) -> int:
    statement = '''
    select level from permissions where username = $1;
    '''
    row = await context['db'].fetchrow(statement, str(user))

    if row is None:
        return 0
    else:
        return row['level']


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
    },
    {
        'trigger': 'uptime',
        'module': 'cmds.uptime',
        'handler': 'UptimeCommand',
        'permissions': 0
    },
    {
        'trigger': 'quit',
        'module': 'cmds.quit',
        'handler': 'QuitCommand',
        'permissions': 2
    },
    {
        'trigger': 'weather',
        'module': 'cmds.weather',
        'handler': 'WeatherCommand',
        'permissions': 0
    },
    {
        'trigger': 'decide',
        'module': 'cmds.decide',
        'handler': 'DecideCommand',
        'permissions': 0
    },
    {
        'trigger': 'roll',
        'module': 'cmds.roll',
        'handler': 'RollCommand',
        'permissions': 0
    },
    {
        'trigger': 'short',
        'module': 'cmds.short',
        'handler': 'ShortCommand',
        'permissions': 0
    },
    {
        'trigger': 'remind',
        'module': 'cmds.remind',
        'handler': 'RemindCommand',
        'permissions': 0
    },
    {
        'trigger': 'insult',
        'module': 'cmds.insult',
        'handler': 'InsultCommand',
        'permissions': 1
    }
]
