from asyncio import Queue
from asyncio import QueueEmpty
from cmds.command import Command
from typing import Optional
from discord import FFmpegPCMAudio
import asyncio
import os
import youtube_dl


song_queue: Queue = Queue(256)
stop_queue: Queue = Queue(1)


async def song_exists(context, link: str) -> bool:
    statement = 'select link from songs where link = $1'
    song = await context['db'].fetchrow(statement, link)

    if song is None:
        return False
    else:
        return True


async def get_song(context, song_id: int):
    statement = 'select id,title from songs where id = $1'
    song = await context['db'].fetchrow(statement, song_id)

    return song


async def play_song(context, message, song_id: int):
    song = await get_song(context, song_id)

    if song is None:
        return None
    else:
        # TODO: Move stop playing and voice connect logic out from
        # this function. Preconditions should be that the bot is
        # already connected to a function and that it is not already
        # playing a song.
        stop_playing(context)

        if len(context['client'].voice_clients) == 0:
            voice = await message.author.voice.channel.connect()
        else:
            voice = context['client'].voice_clients[0]

        path = os.environ.get(
            'MUSIC_DATA_DIR',
            context['config'].get('music_data_dir', 'run/music')
        )
        voice.play(FFmpegPCMAudio('{}/{}.mp3'.format(path, song['id'])),
                   after=lambda e: handle_after_song(context, message))

        return song


# By the time this handler is invoked,
# the database connection that was acquired has already been released.
# We need to acquire a new one.
def handle_after_song(context, message):
    c = after_song(context, message)
    f = asyncio.run_coroutine_threadsafe(c, context['client'].loop)
    try:
        f.result()
    except Exception as e:
        print(e)
        pass


async def after_song(old_context, message):
    try:
        stop_queue.get_nowait()
    except QueueEmpty:
        async with old_context['client'].pool.acquire() as connection:
            new_context = {
                'client': old_context['client'],
                'config': old_context['config'],
                'db': connection
            }

            next_song_id = get_next_song()
            if next_song_id is None:
                pass
            else:
                await play_song(new_context, message, next_song_id)


def stop_playing(context) -> None:
    if len(context['client'].voice_clients) == 1:
        voice = context['client'].voice_clients[0]
        if voice.is_playing():
            voice.stop()


def get_next_song() -> Optional[int]:
    try:
        return song_queue.get_nowait()
    except QueueEmpty:
        return None


async def fetch_song(context, message, link: str):
    if (await song_exists(context, link)) is False:
        await message.channel.send(
            'Downloading {0}...'.format('<' + link + '>')
        )

        with youtube_dl.YoutubeDL({}) as ydl:
            info = ydl.extract_info(link, download=False)
            title = info.get('title')
            duration = info.get('duration')

        statement = '''
            insert into songs (
                title,
                userid,
                uploader,
                link,
                duration
            )
            values($1, $2, $3, $4, $5) returning id;
        '''

        sid = await context['db'].fetch(
            statement,
            title,
            str(message.author.id),
            message.author.name,
            link,
            int(duration),
        )

        path = os.environ.get(
            'MUSIC_DATA_DIR',
            context['config'].get('music_data_dir', 'run/music')
        )
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3'
            }],
            'outtmpl': path + '/' + str(sid[0]['id']) + '.%(ext)s',
            'quiet': False
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        return await message.channel.send(
            '<@{0}> Downloaded {1} ID #{2}.'.format(
                message.author.id,
                title,
                sid[0]['id'],
            )
        )
    else:
        return await message.channel.send(
            'That song already exists in the database.'
        )


async def search_songs(context, query):
    statement = 'select id,title from songs where title ilike \'%{}%\''\
        .format(query.lower())
    songs = await context['db'].fetch(statement)

    return songs


async def list_all_songs(context):
    songs = await context['db'].fetch('''select id,title from songs''')

    return songs


async def queue_song(context, song_id: int) -> None:
    song = await get_song(context, song_id)

    if song is None:
        return None
    else:
        await song_queue.put(song['id'])
        return song


class MusicCommand(Command):
    async def handle(self, context, message):
        usage = 'usage: #music ' \
                '[play|fetch|queue|next|list|stop|' \
                'quit|join|search|lucky|qlucky]'
        content = list(message.content[7:].split())

        if len(content) >= 1:
            if content[0].startswith('play'):
                song = await play_song(context, message, int(content[1]))
                if song is None:
                    return await message.channel.send(
                        'That song does not exist.'
                    )
                else:
                    return await message.channel.send(
                        'Now playing: {}'.format(song['title'])
                    )
            elif content[0].startswith('fetch'):
                if content[1].startswith('https://www.youtube.com/watch?v='):
                    return await fetch_song(context, message, content[1])
                else:
                    return await message.channel.send(
                        'You must specify a valid YouTube video link.'
                    )
            elif content[0].startswith('queue'):
                song = await queue_song(context, int(content[1]))
                if song is None:
                    return await message.channel.send(
                        'The specified song does not exist.'
                    )
                else:
                    return await message.add_reaction('\u2705')
            elif content[0].startswith('next'):
                stop_playing(context)
                next_song_id = get_next_song()
                if next_song_id is None:
                    return message.channel.send('No more songs in queue.')
                else:
                    await stop_queue.put(None)
                    return await play_song(context, message, next_song_id)
            elif content[0].startswith('list'):
                songs = await list_all_songs(context)
                results = '\n'.join([
                    '(' + str(song['id']) + ') - ' +
                    str(song['title']) for song in songs
                ])

                return await message.channel.send(
                    '''```{0}```'''.format(
                        results
                    )
                )
            elif content[0].startswith('stop'):
                for n in range(len(context['client'].voice_clients)):
                    context['client'].voice_clients[n].stop()
                return await message.add_reaction('\u2705')
            elif content[0].startswith('quit'):
                for n in range(len(context['client'].voice_clients)):
                    await context['client'].voice_clients[n].disconnect()
                return await message.add_reaction('\u2705')
            elif content[0].startswith('join'):
                if len(context['client'].voice_clients) > 0:
                    return await message.channel.send(
                        'I am already in a voice channel.'
                    )
                else:
                    return await message.author.voice.channel.connect()
            elif content[0].startswith('search'):
                songs = await search_songs(context, message.content[14:])
                if len(songs) > 0:
                    results = '\n'.join([
                        '(' + str(song['id']) + ') - ' +
                        str(song['title']) for song in songs
                    ])

                    return await message.channel.send(
                        '''```{0}```'''.format(
                            results
                        )
                    )
                else:
                    return await message.channel.send(
                        'No songs were found.'
                    )
            elif content[0].startswith('lucky'):
                songs = await search_songs(context, message.content[13:])
                if len(songs) > 0:
                    await stop_queue.put(None)
                    return await play_song(context, message, songs[0]['id'])
                else:
                    return await message.channel.send(
                        'No songs were found.'
                    )
            elif content[0].startswith('qlucky'):
                songs = await search_songs(context, message.content[14:])
                if len(songs) > 0:
                    print(songs[0]['id'])
                    song = await queue_song(context, songs[0]['id'])
                    if song is None:
                        return await message.channel.send(
                            'The specified song does not exist.'
                        )
                    else:
                        return await message.add_reaction('\u2705')
                else:
                    return await message.channel.send('No songs were found.')

            else:
                return await message.channel.send(usage)
        else:
            return await message.channel.send(usage)
