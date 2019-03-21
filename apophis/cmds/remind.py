""" Reminder Command """
from cmds.command import Command
from datetime import datetime


def convert_times(when):
    t = {
        "year": int(datetime.now().strftime("%Y")),
        "month": int(datetime.now().strftime("%m")),
        "day": int(datetime.now().strftime("%d")),
        "hour": int(datetime.now().strftime("%H")),
        "minute": int(datetime.now().strftime("%M")),
        "second": int(datetime.now().strftime("%S"))
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
        elif iau[x]['unit'].startswith('s'):
            t['second'] = int(iau[x]['int'] + t['second'])

    time_string = "{0}-{1}-{2} {3}:{4}:{5}".format(
        t['year'],
        t['month'],
        t['day'],
        t['hour'],
        t['minute'],
        t['second']
    )

    datetime_object = datetime.strptime(
        time_string,
        "%Y-%m-%d %H:%M:%S"
    ).strftime("%Y-%m-%d %H:%M:%S")

    return datetime_object


async def add_reminder(
    context, author, reminder,
    current, reminder_date, channel
):
    statement = '''
        insert into reminders (
        reminder_date,
        date_of,
        author,
        reminder,
        channel
    )
    values($1, $2, $3, $4, $5);
    '''

    return await context['db'].execute(
        statement,
        reminder_date,
        current,
        str(author),
        reminder,
        str(channel)
    )


class RemindCommand(Command):
    async def handle(self, context, message):
        usage = "usage: !remind <reminder message>, " \
            "<1-* (y) year(s)>, <1-12 (mo) month(s)>, " \
            "<1-364 (d) day(s)>, <1-24 (h) hour(s)>, " \
            "<1-60 (m) minute(s)> <1-60 (s) second(s)>"

        content = message.content[8:].split()
        last = content[-1]
        accepted = [
            'year', 'years', 'y',
            'month', 'months', 'mo',
            'day', 'days', 'd',
            'hour', 'hours', 'h',
            'minute', 'minutes', 'm',
            'second', 'seconds', 's'
        ]

        if last in accepted:
            reminder = message.content[8:].split(', ')
            when = reminder[1:]
            current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if not when:
                return await message.channel.send(usage)

            reminder_time = convert_times(when)

            await add_reminder(
                context,
                message.author.id,
                reminder[0],
                current,
                reminder_time,
                message.channel.id
            )

            return await message.channel.send(
                "Setting reminder, ``{0}`` for, <@{1}>, "
                "duration, {2}, reminder time: {3}"
                .format(
                    reminder[0],
                    message.author.id,
                    when,
                    reminder_time
                )
            )

        return await message.channel.send(usage)
