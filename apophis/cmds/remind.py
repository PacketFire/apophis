""" Reminder Command """
from cmds.command import Command


class RemindCommand(Command):
    async def handler(self, context, message):
        content = message.content[8:].split()

        if len(content) == 2:
            return await message.channel.send(
                "Setting reminder to {0} for {1} at {2}"
                .format(message.author, content[0], content[1])
            )
        else:
            return await message.channel.send(
                "usage: !remind <reminder message> <date/time>"
            )
