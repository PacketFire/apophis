""" Reminder Command """
from cmds.command import Command
import asyncio
import time
import json
import logging


units = {"minutes": 60, "hours": 24, "days": 365, "weeks": 52}
# units = {"minute" : 60, "hour" : 3600, "day" : 86400, "week": 604800, "month": 2592000}


async def add_reminder(author, reminder, when):
    data = {
        "author": author,
        "reminder": reminder,
        "when": when
    }
    try:
        with open("data/reminders.json", "a") as fh:
            fh.write(json.dumps(data))
    except IOError:
        logging.error("Unable to write to reminder file")


class RemindCommand(Command):
    async def handle(self, context, message):
        usage = "usage: !remind <reminder message>, " \
        "<1-* years> <1-12 months> " \
        "<1-52 weeks> <1-364 days> " \
        "<1-24 hours> <1-60 minutes>"

        content = message.content[8:].split()
        last = content[-1]
        accepted = [
            'year', 'years',
            'month', 'months',
            'week', 'weeks',
            'day', 'days',
            'hour', 'hours',
            'minute', 'minutes'
        ]

        if last in accepted:
            reminder = message.content[8:].split(', ')
            when = reminder[1:]

            if not when:
                return await message.channel.send(usage)

            await add_reminder(
                message.author.id, 
                reminder[0],
                when
            )
            
            return await message.channel.send(
                "Setting reminder, ``{0}`` for, <@{1}>, duration, {2}"
                .format(
                    reminder[0],
                    message.author.id,
                    when
                )
            )
        
        return await message.channel.send(usage)
