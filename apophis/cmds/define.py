import requests
import json
from cmds.command import Command

class DefineCommand(Command):
    def __init__(self, cmd_data):
        self.cmd_data = cmd_data

    def parse_command(self, message):
        r = requests.get("http://api.urbandictionary.com/v0/define?term={}".format(message.content[8:]))        
        data = r.json()

        return message.channel.send(message.content[8:] + "[0/" + str(len(data['list'])) +"]: " + data['list'][0]['definition'])


"""        soup = BeautifulSoup(r.content, features="html.parser"

        if len(soup) <= 0:
            return 'no results were found.'

        for i in range(amount):
            return message.channel.send(message.content[8:] + "[0/" + str(amount) + "]: " + soup.find("div",attrs={"class":"meaning"}).text)
        else:
            return message.channel.send(message.content[8:] + "[0/0]" + soup.find("div", attrs={"class":"meaning"}).text)
"""            