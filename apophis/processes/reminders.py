from datetime import datetime
from core.readers import get_reminders
import asyncio


def check_reminders() -> bool:
    current = datetime.now().strftime("%Y-%m-%d %H:%M")

    reminders = get_reminders()

    payload = [
        {
            "date": reminder['date']
        }
        for reminder in reminders
    ]

    if current in payload['date']:
        return True


def output_reminders():
    reminders = get_reminders()

    payload = [
        {
            "author": reminder['author'],
            "reminder": reminder['reminder']
        }
        for reminder in reminders
    ]

    return payload

