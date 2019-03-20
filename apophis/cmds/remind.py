""" Reminder Command """
from cmds.command import Command
import asyncio
import json
import logging
import time
from datetime import datetime


def convert_times(when):
    t = {
        "year": int(datetime.now().strftime("%Y")),
        "month": int(datetime.now().strftime("%m")),
        "day": int(datetime.now().strftime("%d")),
        "hour": int(datetime.now().strftime("%H")),
        "minute": int(datetime.now().strftime("%M")),
    }

    iau = [
        {"int": int(w.split()[0]), "unit": w.split()[1]}
        for w in when
    ]

    for x in range(len(iau)):
        if iau[x]['unit'].startswith('y'):
            t['year'] = int(iau[x]['int'] + t['year'])
        elif iau[x]['unit'].startswith('mo'):
            t['month'] = int(iau[x]['int'] + t['month'])
        elif iau[x]['unit'].startswith('d'):
            t['day'] = int(iau[x]['int'] + t['day'])
        elif iau[x]['unit'].startswith('h'):
            t['hour'] = int(iau[x]['int'] + t['hour'])
        elif iau[x]['unit'].startswith('mi'):
            t['minute'] = int(iau[x]['int'] + t['minute'])

    
    time_string = "{0}-{1}-{2} {3}:{4}".format(
        t['year'],
        t['month'],
        t['day'],
        t['hour'],
        t['minute']
    )

    datetime_object = datetime.strptime(
        time_string,
        "%Y-%m-%d %H:%M"
    ).strftime("%Y-%m-%d %H:%M")

    return datetime_object


async def add_reminder(author, reminder, current, reminder_time):
    data = {
        "author": author,
        "reminder": reminder,
        "date_added": current,
        "reminder_time": reminder_time
    }
    try:
        with open("data/reminders.json", "a") as fh:
            fh.write(json.dumps(data))
    except IOError:
        logging.error("Unable to write to reminder file")


class RemindCommand(Command):
    async def handle(self, context, message):
        usage = "usage: !remind <reminder message>, " \
            "<1-* (y) year(s)>, <1-12 (mo) month(s)>, " \
            "<1-364 (d) day(s)>, <1-24 (h) hour(s)>, " \
            "<1-60 (m) minute(s)>"

        content = message.content[8:].split()
        last = content[-1]
        accepted = [
            'year', 'years', 'y',
            'month', 'months', 'mo',
            'day', 'days', 'd',
            'hour', 'hours', 'h',
            'minute', 'minutes', 'm',
        ]

        if last in accepted:
            reminder = message.content[8:].split(', ')
            when = reminder[1:]
            current = datetime.now().strftime("%Y-%m-%d %H:%M")

            if not when:
                return await message.channel.send(usage)


            reminder_time = convert_times(when)

            await add_reminder(
                message.author.id,
                reminder[0],
                current,
                reminder_time
            )

            return await message.channel.send(
                "Setting reminder, ``{0}`` for, <@{1}>, duration, {2}, reminder time: {3}"
                .format(
                    reminder[0],
                    message.author.id,
                    when,
                    reminder_time
                )
            )


        return await message.channel.send(usage)