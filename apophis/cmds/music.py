from cmds.command import Command

class MusicCommand(Command):
    def __init__(self, cmd_data):
        self.cmd_data = cmd_data

    def parse_command(self, message):
        content = message.content[7:].split(
            " ",
            message.content[7:].count(" ")
        )

        usage = "usage: #music playlist <add/del/play>"
    
        if len(content) == 2:
            if content[0].startswith('playlist'):
                if content[1].startswith('add'):
                    return message.channel.send(content)
                elif content[1].startswith('del'):
                    return message.channel.send(content)
                elif content[1].startswith('play'):
                    return message.channel.send(content)
                else:
                    return message.channel.send(usage)
            else:
                return message.channel.send(usage)
        else:
            return message.channel.send(usage)
