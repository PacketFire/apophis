import asyncio
import asyncpg
import discord
import cmds.command
from core.readers import fetch_config
import os


class BotClient(discord.Client):
    def __init__(self, **kwargs):
        super().__init__()

        self.config = kwargs.pop('config')
        self.pool = kwargs.pop('pool')

    async def on_ready(self):
        print('Logged in as ID: {}, username: {}'.format(self.user.id,
                                                         self.user.name))

    async def on_message(self, message):
        print("#{0} | <{1}> {2}".format(
            message.channel,
            message.author.name,
            message.content
        ))

        async with self.pool.acquire() as connection:
            context = {
                'client': self,
                'config': self.config,
                'db': connection
            }

            await store_messages(
                context,
                str(message.guild.id),
                message.guild.name,
                str(message.author.id),
                message.author.name,
                message.content
            )

            if message.author.id != self.user.id:
                prefix = self.config.get('prefix', '!')
                commands = cmds.command.commands

                for p in prefix:
                    if not message.content.startswith(p):
                        continue

                    for cm in commands:
                        if not message.content[1:].startswith(cm['trigger']):
                            continue

                        c = cmds.command.command_handler(cm['module'],
                                                         cm['handler'])

                        perms = await cmds.command.get_permissions(
                            context,
                            message.author.id
                        )

                        if perms < cm['permissions']:
                            return await message.channel.send('Unauthorized')

                        await c.handle(cm, context, message)


async def run():
    config = fetch_config()
    bot_token = os.environ.get('BOT_TOKEN', config.get('bot_token'))

    if bot_token is None:
        print('You must specify a bot token in order to start the bot.')
        return

    pool = await connect_db(config)
    print('Connected to postgres')

    client = BotClient(config=config, pool=pool)
    await client.start(bot_token)


async def connect_db(config):
    db_host = os.environ.get(
        'DB_HOST',
        config.get(
            'db_host',
            'postgresql://postgres:postgres@localhost:15432/apophis'
        )
    )

    return await asyncpg.create_pool(db_host)


async def store_messages(context, sid, server, uid, user, content):
    statement = '''
    insert into messages (
        guildid,
        guildname,
        userid,
        username,
        content
    )
    values ($1, $2, $3, $4, $5)
    '''

    return await context['db'].execute(
        statement,
        sid,
        server,
        uid,
        user,
        content
    )


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        print('Exiting bot, caught keyboard interrupt.')
        os._exit(0)
