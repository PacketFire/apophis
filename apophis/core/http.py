from aiohttp import web


async def index(request):
    return web.Response(text="Apophis Web")


async def http_handler():
    app = web.Application()
    app.add_routes([web.get('/', index)])
    
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, '127.0.0.1', 5002)
    await site.start()

    print('Serving on http://127.0.0.1:5002/')

    # TODO: Handle finish signal here
