from datetime import datetime
from core.readers import get_reminders
import asyncio
import logging


async def output_reminder(context):
    logging.info("Polling reminders..")
    while True:
        await asyncio.sleep(1)
        current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        reminders = await get_reminders(context)

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
