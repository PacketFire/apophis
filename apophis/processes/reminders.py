from datetime import datetime
from core.readers import get_reminders
import asyncio
import logging

async def output_reminder(context):
    logging.info('Starting reminders poll..')
    current = datetime.now().strftime("%Y-%m-%d %H:%M")
    reminders = get_reminders()

    payload = [
        {
            "author": reminder['author'],
            "reminder": reminder['reminder'],
            "reminder_time": reminder['reminder_time']
        }
        for reminder in reminders
    ]

    if current is payload['reminder_time']:
        channel = context['client'].get_channel(550196694118170624)
        return await channel.send(
            "<@{0}> {1}".format(
                payload['author'],
                payload['reminder']
            )
        )