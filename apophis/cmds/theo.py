import random
import asyncio
from cmds.command import Command

class TheoCommand(Command):
    def __init__(self, cmd_data):
        self.cmd_data = cmd_data

    async def parse_command(self, message) -> str:
        try:
            with open('data/theo.txt', 'r') as fh:
                line = random.choice(list(fh))
        except IOError:
            return 'unable to open data file'

        return await message.channel.send(line)
