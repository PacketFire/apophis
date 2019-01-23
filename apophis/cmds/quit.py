from cmds.command import Command


class QuitCommand(Command):
    async def handle(self, context, message):
        await message.channel.send(
            'Goodbye master.'
        )
        await context['client'].logout()