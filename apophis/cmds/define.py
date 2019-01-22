import requests
from cmds.command import Command


class DefineCommand(Command):
    def handle(self, context, message):
        content = message.content[8:].split()

        try:
            index = int(content[-1])
            term = ' '.join(content[:-1])
        except ValueError:
            index = 1
            term = ' '.join(content)

        r = requests.get(
            "http://api.urbandictionary.com/v0/define?term={}"
            .format(term)
        )
        data = r.json()
        definitions = data.get("list", [])
        total = len(definitions) if definitions else 0

        if total == 0:
            reply = "{0} is not defined yet".format(term)
        elif index > total or index < 1:
            reply = "cannot find defintion on index {0}".format(index)
        else:
            definition = definitions[index-1].get("definition")
            reply = f"{term} [{index}/{total}]: {definition}"

        return message.channel.send(reply)
