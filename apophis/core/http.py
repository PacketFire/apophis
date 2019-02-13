from aiohttp import web
import logging


async def index(request):
    return web.Response(text="Apophis Web")


async def login(request):
    data = await request.json()

    return web.json_response(data)


async def http_handler():
    app = web.Application()
    app.add_routes([web.get('/', index)])
    app.add_routes([web.post('/login', login)])

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, '127.0.0.1', 5002)
    await site.start()

    logging.info('Serving on http://127.0.0.1:5002/')

    # TODO: Handle finish signal here
