""" Access Command """
from cmds.command import Command, check_permissions


class AccessCommand(Command):
    async def handle(self, context, message) -> str:
        content = list(message.content[8:].split())
        al = await check_permissions(message.author.name, context)
        print(al)
        if al == 2:
            if len(content) >= 1:
                if content[0] == 'list':
                    statement = 'select * from permissions'
                    rows = await context['db'].fetch(statement)

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
