from cmds.command import Command


class HelpCommand(Command):
    def __init__(self, cmd_data):
        self.cmd_data = cmd_data

    def parse_command(self, message):
        output = [
            "!help - usage: !help <command>",
            "!theo - usage: !theo",
        ]

        return message.channel.send("```" + "\n".join(output) + "```")
