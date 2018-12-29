import discord
import asyncio
import cmds.command

class BotClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        
    
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        else:
            for i in range(len(cmds.command.commands)):
                if message.content.startswith(cmds.command.commands[i]['trigger']):
                    c = cmds.command.command_handler(
                        cmds.command.commands[i]['module'], 
                        cmds.command.commands[i]['handler']
                    )
                    c(message, cmds.command.commands[i])
                    await message.channel.send(c.parse_command(cmds.command.commands[i]))

        return print("#" + str(message.channel) + " | <" + message.author.name + "> " + message.content)


