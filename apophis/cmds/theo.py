import random
from cmds.command import Command

class TheoCommand(Command):
    def __init__(self, message, cmd_data):
        self.message = message
        self.cmd_data = cmd_data

    def parse_command(self) -> str:
        return random.choice(list(open('data/theo.txt', 'r')))
