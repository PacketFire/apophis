import discord
import asyncio
from cmd import parse_commands

class Bot(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)

    async def on_message(self, message):
        if message.author == self.user:
            return

        cmd.parse_commands(message.content)
