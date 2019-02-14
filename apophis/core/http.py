from aiohttp import web
import logging


async def index(request):
    return web.Response(text="Apophis Web")


async def search(request):
    data = await request.json()

    statement = 'select username,content from messages where content ilike \'%{}%\''\
        .format(data['term'])
    
    results = await request.app['pool'].fetch(statement)
    payload = []

    if len(results) > 0:
        for result in results:
            payload.append({
                'username': result['username'],
                'content': result['content']
            })

    return web.json_response(payload)


async def http_handler(db):
    app = web.Application()
    app.add_routes([web.get('/', index)])
    app.add_routes([web.post('/search', search)])
    app['pool'] = db

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, '127.0.0.1', 5002)
    await site.start()

    logging.info('Serving on http://127.0.0.1:5002/')

    # TODO: Handle finish signal here
