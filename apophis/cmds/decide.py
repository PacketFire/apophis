""" Decide Command """
from cmds.command import Command
import random


class DecideCommand(Command):
    async def handle(self, context, message):
        content = message.content[8:].split()

        usage = 'usage: decide [option1,' \
            'option2,option3...]'

        if len(content) >= 1:
            options = message.content[8:].split(',')
            option = random.choice(options)

            return await message.channel.send(option)

        else:
            return await message.channel.send(usage)
