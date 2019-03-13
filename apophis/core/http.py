from aiohttp import web
import logging


async def permlist(request):
    statement = 'select id,username,level from permissions'
    results = await request.app['pool'].fetch(statement)
    payload = []

    if len(results) > 0:
        for result in results:
            payload.append({
                'id': result['id'],
                'username': result['username'],
                'level': result['level']
            })

    return web.json_response(
        payload,
        headers={
            'Access-Control-Allow-Origin': '*'
        }
    )


async def addperm(request):
    data = await request.json()
    statement = '''
    insert into permissions (username, level)
    values($1, $2);
    '''
    await request.app['pool'].execute(
        statement,
        data['username'],
        int(data['level'])
    )

    payload = {
        'username': data['username'],
        'level': data['level']
    }

    return web.json_response(
        payload,
        headers={
            'Access-Control-Allow-Origin': '*'
        }
    )


async def search(request):
    data = await request.json()

    statement = 'select username,content from messages' \
        'where content ilike \'%{}%\''\
        .format(data['term'])

    results = await request.app['pool'].fetch(statement)
    payload = [
        {'username': result['username'], 'content': result['content']}
        for result in results
    ]

    return web.json_response(
        payload,
        headers={
            'Access-Control-Allow-Origin': '*'
        }
    )


async def delperm(request):
    id = request.match_info.get('id')
    statement = 'delete * from permissions where username = {}' \
        .format(id)

    await request.app['pool'].execute(statement)


async def http_handler(db):
    app = web.Application()
    app.add_routes([web.post('/search', search)])
    app.add_routes([web.get('/permissions', permlist)])
    app.add_routes([web.post('/permissions', addperm)])
    app.add_routes([web.delete('/permissions/{id}', delperm)])
    app['pool'] = db

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, '127.0.0.1', 5002)
    await site.start()

    logging.info('Serving on http://127.0.0.1:5002/')

    # TODO: Handle finish signal here
