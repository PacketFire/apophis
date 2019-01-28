from aiohttp import web


async def index(request):
    return web.Response(text="Apophis Web")


async def http_handler():
    app = web.Application()
    app.add_routes([web.get('/', index)])

    print("Running httpd...")
    web.run_app(app, host="127.0.0.1", port="5000")
