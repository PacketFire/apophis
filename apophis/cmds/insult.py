import random
from cmds.command import Command


class InsultCommand(Command):
    async def handle(self, context, message) -> str:

        receipents = " ".join(["<@{}>".format(m.id) for m in message.mentions])

        try:
            with open("data/insults.txt", "r") as fh:
                line = random.choice(list(fh))
        except IOError:
            line = "unable to open data file"

        sent_msg = "{}, {}".format(receipents, line) if receipents else line
        return await message.channel.send(sent_msg)
