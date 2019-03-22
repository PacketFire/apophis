from datetime import datetime
import asyncio
import logging
from typing import List, Any


async def get_reminders(context, current) -> List[Any]:
    statement = '''
    select reminder_date, author, reminder, channel from reminders
    where reminder_date >= $1
    '''
    dates = await context['db'].fetch(statement, current)

    return dates


async def output_reminder(context):
    logging.info("Polling reminders..")
    while True:
        await asyncio.sleep(60)
        current = datetime.now().strftime("%Y-%m-%d %H:%M")

        reminders = await get_reminders(context, current)

        if len(reminders) > 0:
            payload = [
                {
                    "author": reminder['author'],
                    "reminder": reminder['reminder'],
                    "reminder_date": reminder['reminder_date'],
                    "channel": reminder['channel']
                }
                for reminder in reminders
            ]

            for i in range(len(payload)):
                if current in payload[i]['reminder_date']:
                    channel = context['client'].get_channel(
                        int(payload[i]['channel'])
                    )
                    await channel.send(
                        "<@{0}> {1}".format(
                            payload[i]['author'],
                            payload[i]['reminder']
                        )
                    )
