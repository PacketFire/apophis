""" Roll Command """
from cmds.command import Command
import random


class RollCommand(Command):
    async def handle(self, context, message):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        dice = die1 + die2

        return await message.channel.send(
            'You rolled **{}** and **{}** with a total result of **{}**.'
            .format(die1, die2, dice)
        )
