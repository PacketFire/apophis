""" Reminder Command """
from cmds.command import Command
# import asyncio
# import time
import json
import logging


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
            "<1-* year(s)>, <1-12 month(s)>, " \
            "<1-52 week(s)>, <1-364 day(s)>, " \
            "<1-24 hour(s)>, <1-60 minute(s)>"

        content = message.content[8:].split()
        last = content[-1]
        accepted = [
            'year', 'years', 'y',
            'month', 'months', 'mo',
            'week', 'weeks', 'w',
            'day', 'days', 'd',
            'hour', 'hours', 'h',
            'minute', 'minutes', 'm',
            'second', 'seconds', 's'
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
