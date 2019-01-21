import asyncio
import asyncpg
import discord
import cmds.command
from core.readers import fetch_config
import os


config = fetch_config()
client = discord.Client()
pool = None


@client.event
async def on_ready():
    print('Logged in as ID: {}, username: {}'.format(client.user.id,
                                                     client.user.name))

    db_host = os.environ.get(
        'DB_HOST',
        config.get(
            'db_host',
            'postgresql://postgres:postgres@localhost:15432/apophis'
        )
    )

    global pool
    pool = await asyncpg.create_pool(db_host)

    print('Connected to database')


@client.event
async def on_message(message):
    print("#{0} | <{1}> {2}".format(message.channel,
                                    message.author.name,
                                    message.content))

    if message.author.id == client.user.id:
        return
    else:
        prefix = config['prefix']
        commands = cmds.command.commands
        for n in range(len(prefix)):
            if message.content.startswith(prefix[n]):
                for i in range(len(commands)):
                    if message.content[1:].startswith(
                            commands[i]['trigger']
                    ):
                        c = cmds.command.command_handler(
                            commands[i]['module'],
                            commands[i]['handler']
                        )

                        async with pool.acquire() as connection:
                            context = {
                                'client': client,
                                'config': config,
                                'db': connection
                            }


                            perms = await cmds.command.check_permissions(
                                context, message.author.id
                            )

                            if perms >= commands[i]['permissions']:
                                await c.handle(
                                    commands[i],
                                    context,
                                    message,
                                )
                            else:
                                return await message.channel.send(
                                    'Unauthorized.'
                                )


if __name__ == "__main__":
    bot_token = os.environ.get('BOT_TOKEN', config['bot_token'])

    if bot_token is None:
        print('You must specify a bot token in order to start the bot.')
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(client.start(config['bot_token']))
