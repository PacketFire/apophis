import random
from cmds.command import Command


class TheoCommand(Command):
    async def handle(self, context, message) -> str:
        try:
            with open('data/theo.txt', 'r') as fh:
                line = random.choice(list(fh))
        except IOError:
            line = 'unable to open data file'

        return await message.channel.send(line)
