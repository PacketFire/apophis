""" Reminder Command """
from cmds.command import Command
import asyncio
import time


async def reminder_timer(loop, calltime):
    now = loop.time()
    loop.call_at(now + calltime)


async def reminder_callback(calltime):
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            reminder_timer(event_loop, calltime)
        )
    finally:
        event_loop.close()


class RemindCommand(Command):
    async def handle(self, context, message):
        content = message.content[8:].split()
        accepted = [
            'years',
            'year',
            'days',
            'day',
            'hour',
            'hours',
            'minute',
            'minutes'
        ]

        if content[-1] in accepted:
            
            return await message.channel.send(
                "Setting reminder ``{0}`` for <@{1}>"
                .format(
                    message.content[8:],
                    message.author.id
                )
            )
        else:
            return await message.channel.send(
                "usage: !remind <reminder message> "
                "<1-* years> <1-364 days> <1-24 hours> <1-60 minutes>"
            )
