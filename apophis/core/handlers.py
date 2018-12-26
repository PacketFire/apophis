import cmds

triggers = ['test']

async def parse_commands(message):
   if message.content.startswith('!'):
      for trigger in triggers:
         cmds.trigger.init(message)
