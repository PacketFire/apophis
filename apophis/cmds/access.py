""" Access Command """
from cmds.command import Command, check_permissions
from core.storage import connect


class AccessCommand(Command):
    def __init__(self, cmd_data):
        self.cmd_data = cmd_data

    async def parse_command(self, message):
        content = list(message.content[8:].split())
        al = await check_permissions(message.author.name, 'access')

        if al == 2:
            if len(content) >= 1:
                if content[0] == 'list':
                    db = await connect()
                    statement = 'select * from permissions'
                    rows = await db.fetch(statement)
                    await db.close()
                    
                    output = '\n'.join([
                        str(row['username']) + ': level ' +
                        str(row['level']) for row in rows
                    ])

                    return await message.channel.send(
                        '```' + output + '```'
                    )
            else:
                return await message.channel.send(
                    'usage: access <list/add/del> parameters'
                )
        else:
            return await message.channel.send(
                'You do not have permission to use that command.'
            )
