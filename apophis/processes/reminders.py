from datetime import datetime
from core.readers import get_reminders
import asyncio
import logging


async def output_reminder(context):
    logging.info("Polling reminders..")

    while True:
        await asyncio.sleep(1)
        current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reminders = get_reminders()

        payload = [
            {
                "author": reminder['author'],
                "reminder": reminder['reminder'],
                "reminder_time": reminder['reminder_time']
            }
            for reminder in reminders
        ]

        for i in range(len(payload)):
            if current in payload[i]['reminder_time']:
                channel = context['client'].get_channel(523599882162929664)
                await channel.send(
                    "<@{0}> {1}".format(
                        payload[i]['author'],
                        payload[i]['reminder']
                    )
                )
