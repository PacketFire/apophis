import youtube_dl
from cmds.command import Command
from typing import Optional
from discord import FFmpegPCMAudio


async def song_exists(context, link: str) -> bool:
    statement = 'select link from songs where link = $1'
    song = await context['db'].fetchrow(statement, link)

    if song is None:
        return False
    else:
        return True


async def get_song(context, song_id: int) -> Optional[any]:
    statement = 'select id,title from songs where id = $1'
    song = await context['db'].fetchrow(statement, song_id)

    return song


async def play_song(context, message, song_id: int):
    song = await get_song(context, song_id)

    if song is None:
        return await message.channel.send(
            'The specified song could not be found.'
        )
    else:
        if len(context['client'].voice_clients) == 1:
            voice = context['client'].voice_clients[0]
            if voice.is_playing():
                voice.stop()
        else:
            voice = await message.author.voice.channel.connect()

        voice.play(FFmpegPCMAudio('data/music/{}.mp3'.format(song['id'])))
        return await message.channel.send(
            'Now playing: {0}'.format(song['title'])
        )


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

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'data/music/' + str(sid[0]['id']) + '.%(ext)s',
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


async def list_all_songs(context):
    songs = await context['db'].fetch('''select id,title from songs''')

    return songs


class MusicCommand(Command):
    async def handle(self, context, message):
        usage = "usage: #music playlist <add/del/play>"
        content = list(message.content[7:].split())

        if len(content) >= 1:
            if content[0].startswith('play'):
                await play_song(context, message, int(content[1]))
            elif content[0].startswith('fetch'):
                if content[1].startswith('https://www.youtube.com/watch?v='):
                    await fetch_song(context, message, content[1])
                else:
                    return await message.channel.send(
                        "must contain valid youtube url"
                    )
            elif content[0].startswith('list'):
                if content[1].startswith('all'):
                    songs = await list_all_songs(context)
                    stitle = '\n'.join([
                        '(' + str(song['id']) + ') - ' +
                        str(song['title']) for song in songs
                    ])

                    await message.channel.send(
                        '''```{0}```'''.format(
                            stitle
                        )
                    )
            elif content[0].startswith('stop'):
                for n in range(len(context['client'].voice_clients)):
                    context['client'].voice_clients[n].stop()
            elif content[0].startswith('quit'):
                for n in range(len(context['client'].voice_clients)):
                    await context['client'].voice_clients[n].disconnect()
            elif content[0].startswith('join'):
                await message.author.voice.channel.connect()
            else:
                return await message.channel.send(usage)
        else:
            return await message.channel.send(usage)
