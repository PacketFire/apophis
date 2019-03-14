""" Reminder Command """
from cmds.command import Command


class RemindCommand(Command):
    async def handle(self, context, message):
        if message.content[-2:] == "pm" or message.content[-2:] == "am":
            return await message.channel.send(
                "Setting reminder ``{0}`` for <@{1}>"
                .format(
                    message.content[8:],
                    message.author.id
                )
            )
        else:
            return await message.channel.send(
                "usage: !remind <reminder message> "
                "<date (00/00/0000)> <time (1:00-12:00 am or pm)>"
            )
