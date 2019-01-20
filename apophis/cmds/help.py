from cmds.command import Command


class HelpCommand(Command):
    def handle(self, context, message):
        output = [
            "!help - usage: !help <command>",
            "!theo - usage: !theo",
        ]

        return message.channel.send("```" + "\n".join(output) + "```")
