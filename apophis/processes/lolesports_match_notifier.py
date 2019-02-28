""" lolesports match notifier Process """
import aiohttp
import asyncio
import logging
import os


logger = logging.getLogger(__name__)
relapi = 'https://prod-relapi.ewp.gg/persisted/gw'
relapi_js = 'https://watch.na.lolesports.com/Common/Service/RelApi/RelApi.js'
environment = 'prod'
subscribed_leagues = [
    'LCS',
    'LEC',
    'LCK'
    ]

channel_id = int(os.environ.get(
    'LOLESPORTS_NOTIFICATION_CHANNEL_ID', 
    '550196694118170624'
))


async def get_api_key(client) -> str:
    async with client.get(relapi_js) as response:
        return '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'


async def get_live_events(client):
    api_key = await get_api_key(client)

    headers = {'x-api-key': api_key}

    async with client.get(f'{relapi}/getLive?hl=en-US', headers=headers) as response:
        return await response.json()


def get_event_message(event):
    league = event['league']['name']
    block_name = event['blockName']
    team_a = event['match']['teams'][0]['code']
    team_b = event['match']['teams'][1]['code']
                
    return f'**{league} {block_name}** - **{team_a} vs {team_b}** has started (<https://watch.na.lolesports.com/en_US/{league}/en>)'

async def start(context) -> None:
    logger.info('Started lolesports match notifier process...')

    async with aiohttp.ClientSession() as client:
        live_events = await get_live_events(client)

    last_events = []        
    initial_events = live_events['data']['schedule']['events']
    if initial_events is not None:
        last_events = initial_events

    while True:
        await asyncio.sleep(10)

        try:
            async with aiohttp.ClientSession() as client:
                live_events = await get_live_events(client)

            current_events = live_events['data']['schedule']['events']
            if current_events is None:
                last_events = []
                continue
                
            for event in current_events:
                league = event['league']['name']
                if league not in subscribed_leagues:
                    continue
                
                match_id = event['match']['id']
                if any(el['match']['id'] == match_id for el in last_events):
                    continue

                channel = context['client'].get_channel(channel_id)
                await channel.send(get_event_message(event))
                
            last_events = current_events
        except Exception as e:
            logger.error('Failed to process live game data.', exc_info=1)
