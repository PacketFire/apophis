import discord
import asyncio
import core.handlers

class Bot(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        ch = core.handlers.CmdHandler(Bot())
        await ch.parse_cmds(message)
