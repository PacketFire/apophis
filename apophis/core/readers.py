import json
import logging
from typing import List, Any


def fetch_config():
    try:
        with open('data/config.json', 'r') as fh:
            config = json.load(fh)
        return config
    except IOError:
        return {'error': 'config does not exist'}


def get_reminders() -> List[Any]:
    try:
        with open('data/reminders.json', 'r') as fh:
            reminders = json.load(fh)
    except IOError:
        logging.error("Unable to read reminders file")

    return reminders
