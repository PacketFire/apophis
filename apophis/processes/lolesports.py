""" League of Legends Esports Process """
import aiohttp
import asyncio
import logging


logger = logging.getLogger(__name__)
relapi = 'https://prod-relapi.ewp.gg/persisted/gw'
relapi_js = 'https://watch.na.lolesports.com/Common/Service/RelApi/RelApi.js'
environment = 'prod'
subscribed_leagues = [
    '98767991299243165', # LCS
    '98767991310872058', # LCK
    '98767991302996019'  # LEC
    ]


async def get_api_key(client) -> str:
    async with client.get(relapi_js) as response:
        return '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'


async def get_live_events(client):
    api_key = await get_api_key(client)

    headers = {'x-api-key': api_key}

    async with client.get(f'{relapi}/getLive?hl=en-US', headers=headers) as response:
        return await response.json()


async def start(context) -> None:
    logger.info('Started lolesports process...')

    last_events = []

    while True:
        try:
            async with aiohttp.ClientSession() as client:
                live_events = await get_live_events(client)

            logger.info(live_events)

            current_events = live_events['data']['schedule']['events']
            if current_events is not None:
                logger.info('Found playing events')
                # If there are any events in current_events that aren't in last_events, a new event has started.
                # If the event occurs in a league we are interested in, send a notification.
        except Exception as e:
            logger.error('Failed to process live game data.', exc_info=1)

        await asyncio.sleep(10)
