import cmds
from typing import List

class CmdHandler:
   def __init__(self, bot):
      self.bot = bot
      self.cmds = ['!help', '!test']

   def add_cmd(self, cmd):
      self.cmds.append(cmd)
   
   def get_cmds(self) -> List:
      return self.cmds

   def parse_cmds(self, message) -> str:
      for cmd in self.cmds:
         if message.content.startswith(cmd):
            return self.bot.send_message(message.channel)
