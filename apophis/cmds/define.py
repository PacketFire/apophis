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
            f"http://api.urbandictionary.com/v0/define?term={term}"
        )
        data = r.json()
        definitions = data.get("list", [])
        total = len(definitions) if definitions else 0

        if total == 0:
            reply = f"{term} is not defined yet"
        elif index > total or index < 1:
            reply = f"cannot find defintion on index {index}"
        else:
            definition = definitions[index-1].get("definition")
            reply = f"{term} [{index}/{total}]: {definition}"

        return message.channel.send(reply)
