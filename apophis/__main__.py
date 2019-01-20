import asyncio
import asyncpg
import discord
import cmds.command
import sys


client = discord.Client()
pool = None


@client.event
async def on_ready():
    print('Logged in as ID: {}, username: {}'.format(client.user.id,
                                                     client.user.name))

    global pool
    pool = await asyncpg.create_pool(
        'postgresql://postgres:postgres@localhost:15432/apophis'
    )

    print('Connected to database')


@client.event
async def on_message(message):
    print("#{0} | <{1}> {2}".format(message.channel,
                                    message.author.name,
                                    message.content))

    if message.author.id == client.user.id:
        return
    else:
        for n in range(len(cmds.command.prefix)):
            if message.content.startswith(cmds.command.prefix[n]):
                for i in range(len(cmds.command.commands)):
                    if message.content[1:].startswith(
                            cmds.command.commands[i]['trigger']
                    ):
                        c = cmds.command.command_handler(
                            cmds.command.commands[i]['module'],
                            cmds.command.commands[i]['handler']
                        )

                        async with pool.acquire() as connection:
                            context = {
                                'client': client,
                                'db': connection
                            }

                            await c.handle(
                                cmds.command.commands[i],
                                context,
                                message,
                            )


if __name__ == "__main__":
    if len(sys.argv) == 2:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(client.start(sys.argv[1]))
    else:
        print("To start bot a token is required.")
