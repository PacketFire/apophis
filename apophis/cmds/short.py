"""
URL Shortener Command
Utilizing http://pfurl.me API
"""
from cmds.command import Command
from urllib.parse import urlparse
import requests


async def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class ShortCommand(Command):
    async def handle(self, context, message):
        content = message.content[7:].split()
        print(len(content))
        if len(content) >= 1:
            if await validate_url(content[0]) is not False:
                payload = {
                    'url': content[0]
                }
                response = requests.post(
                    'http://pfurl.me',
                    json=payload
                )
                return await message.channel.send(
                    'Your URL: <' + response.text.strip('"') + '>'
                )
