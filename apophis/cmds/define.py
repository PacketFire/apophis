import requests
from cmds.command import Command


class DefineCommand(Command):
    def handle(self, context, message):
        content = list(message.content[8:].split())
        last = content[-1]
        r = requests.get(
            "http://api.urbandictionary.com/v0/define?term={}"
            .format(content)
        )
        data = r.json()

        if last.isdigit():
            return message.channel.send(
                message.content[8:-1] +
                "[" + str(last) + "/" +
                str(len(data['list'])-1) +
                "]: " + data['list'][int(last)]['definition']
            )
        else:
            return message.channel.send(
                message.content[8:] +
                "[0/" + str(len(data['list'])-1) + "]: " +
                data['list'][0]['definition']
            )
