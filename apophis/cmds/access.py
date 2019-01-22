""" Access Command """
from cmds.command import Command


class AccessCommand(Command):
    async def handle(self, context, message) -> str:
        content = list(message.content[8:].split())

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
            elif content[0] == 'add':
                statement = '''
                insert into permissions (username, level)
                values($1, $2);
                '''

                user = content[1].strip('<@>')
                await context['db'].execute(
                    statement,
                    user,
                    int(content[2])
                )

                return await message.channel.send(
                    'Added {0} with access level {1} to database.'
                    .format(content[1], content[2])
                )
            elif content[0] == 'del':
                statement = '''
                delete from permissions where username = $1
                '''
                user = content[1].strip('<@>')
                await context['db'].execute(
                    statement,
                    user
                )

                return await message.channel.send(
                    'Removed {0} from the permissions database.'
                    .format(content[1])
                )
        else:
            return await message.channel.send(
                'usage: access <list/add/del> parameters'
            )
