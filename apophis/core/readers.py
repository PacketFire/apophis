import json
from typing import List, Any


def fetch_config():
    try:
        with open('data/config.json', 'r') as fh:
            config = json.load(fh)
        return config
    except IOError:
        return {'error': 'config does not exist'}


async def get_reminders(context) -> List[Any]:
    statement = '''
    select reminder_date, author, reminder, channel from reminders
    '''
    dates = await context['db'].fetch(statement)

    return dates
