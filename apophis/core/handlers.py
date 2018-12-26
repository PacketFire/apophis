

async def parse_commands(message):
   if message.content.startswith('!test'):
      await message.channel.send('testing..')
