import json


def fetch_config():
    try:
        with open('data/config.json', 'r') as fh:
            config = json.load(fh)
        return config
    except IOError:
        return 'config does not exist'
