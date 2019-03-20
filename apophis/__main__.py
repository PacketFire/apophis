import asyncio
import asyncpg
import calendar
import discord
import os
import time
import logging
import cmds.command
import processes.lolesports_match_notifier
from core.readers import fetch_config
from core.http import http_handler
from processes.reminders import output_reminder


log_level = os.environ.get('LOGLEVEL', 'INFO')
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='[%(asctime)s %(filename)s'
    ':%(lineno)s - %(funcName)20s() ] %(message)s',
    level=log_level,
    handlers=[
        logging.StreamHandler()
    ]
)

start_time = calendar.timegm(time.gmtime())


class BotClient(discord.Client):
    def __init__(self, **kwargs):
        super().__init__()

        self.config = kwargs.pop('config')
        self.pool = kwargs.pop('pool')

    async def on_ready(self):
        logger.debug(
            'Logged in as ID: %s, username: %s',
            self.user.id, self.user.name
        )

    async def on_message(self, message):
        logger.debug(
            "#%s | <%s> %s",
            message.channel,
            message.author.name,
            message.content
        )

        async with self.pool.acquire() as connection:
            context = {
                'client': self,
                'config': self.config,
                'db': connection,
                'start_time': start_time
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
                prefix = self.config.get('prefix', ['!'])
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


async def start_processes(client):
    context = {
        'client': client
    }

    return await processes.lolesports_match_notifier.start(context)


async def poll_reminders(client):
    context = {
        'client': client
    }

    return await output_reminder(context)


async def connect_db(config):
    address = os.environ.get(
        'POSTGRES_ADDRESS',
        'localhost:15432'
    )
    username = os.environ.get(
        'POSTGRES_USERNAME',
        'postgres'
    )
    password = os.environ.get(
        'POSTGRES_PASSWORD',
        'postgres'
    )
    database = os.environ.get(
        'POSTGRES_DATABASE',
        'apophis'
    )

    dsn = 'postgresql://{}:{}@{}/{}'.format(
        username,
        password,
        address,
        database
    )

    try:
        return await asyncpg.create_pool(dsn)
    except Exception as e:
        logger.error(e)
        raise e


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


async def run_coroutines():
    config = fetch_config()

    bot_token = os.environ.get('BOT_TOKEN', config.get('bot_token'))
    if bot_token is None:
        logger.error(
            'You must specify a bot token in order to start the bot.'
        )
        return

    pool = await connect_db(config)
    client = BotClient(config=config, pool=pool)

    tasks = [
        client.start(bot_token),
        start_processes(client),
        http_handler(pool),
        poll_reminders(client)
    ]
    return await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_coroutines())
    except KeyboardInterrupt:
        logger.debug('Exiting bot, caught a keyboard interrupt.')
        os._exit(0)
    except Exception as e:
        logger.error(e)
