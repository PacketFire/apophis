import requests
import json
from cmds.command import Command

class DefineCommand(Command):
    def __init__(self, cmd_data):
        self.cmd_data = cmd_data

    def parse_command(self, message):
        content = message.content[8:].split(" ", message.content[8:].count(" "))
        last = content[-1]
        r = requests.get("http://api.urbandictionary.com/v0/define?term={}".format(content))        
        data = r.json()

        if last.isdigit():
            return message.channel.send(message.content[8:-1] + "[" + str(last) + "/" + str(len(data['list'])) + "]: " + data['list'][int(last)]['definition'])
        else:
            return message.channel.send(message.content[8:] + "[0/" + str(len(data['list'])) +"]: " + data['list'][0]['definition'])
