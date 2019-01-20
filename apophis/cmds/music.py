import json
import youtube_dl
from cmds.command import Command
from typing import NamedTuple
from typing import Optional
from discord import FFmpegPCMAudio
from core.storage import connect


class PlaylistData(NamedTuple):
    url: str


def read_playlist_file(filename: str) -> PlaylistData:
    try:
        with open('data/music/' + filename + '.json', 'r') as fh:
            data = json.load(fh)
            return PlaylistData(data['url'])
    except IOError:
        return PlaylistData('')


def write_playlist_file(filename: str, playlist_data: PlaylistData) -> None:
    file_data = {
        'url': playlist_data,
    }

    try:
        with open('data/music/' + filename + '.json', 'a+') as fh:
            fh.write(json.dumps(file_data))
    except IOError:
        print("unable to write to file")


def playlist_file_exists(filename: str) -> bool:
    try:
        fh = open('data/music/' + filename + '.json', 'r')
        fh.close()
        return True
    except IOError:
        return False


async def song_exists(link: str) -> bool:
    statement = 'select link from songs where link = $1'
    db = await connect()
    song = await db.fetchrow(statement, link)
    await db.close()

    if song is None:
        return False
    else:
        return True


async def get_song(id: int) -> Optional[any]:
    statement = 'select id, title from songs where id = $1'
    db = await connect()
    song = await db.fetchrow(statement, id)
    await db.close()

    return song


async def play_song(message, id: int):
    song = await get_song(id)

    if song is None:
        return await message.channel.send(
            'The specified song could not be found.'
        )
    else:
        voice = await message.author.voice.channel.connect()
        voice.play(FFmpegPCMAudio('data/music/{}.mp3'.format(song['id'])))
        return await message.channel.send(
            'Playing {0}...'.format(song['title'])
        )


async def fetch_song(message, link: str):
    if (await song_exists(link)) is False:
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

        db = await connect()
        sid = await db.fetch(
            statement,
            title,
            str(message.author.id),
            message.author.name,
            link,
            int(duration),
        )
        await db.close()

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


async def list_all_songs():
    db = await connect()
    songs = await db.fetch('''select id,title from songs''')
    await db.close()

    return songs


class MusicCommand(Command):
    def __init__(self, cmd_data):
        self.cmd_data = cmd_data

    async def parse_command(self, message):
        usage = "usage: #music playlist <add/del/play>"
        content = list(message.content[7:].split())

        if len(content) >= 2:
            if content[0].startswith('playlist'):
                if content[1].startswith('add'):
                    if playlist_file_exists(content[2]):
                        write_playlist_file(content[2], content[3])
                        return await message.channel.send(
                            'Adding ``{0}`` to playlist ``{1}``'
                            .format(content[3], content[2])
                        )
                    else:
                        write_playlist_file(content[2], content[3])
                        return await message.channel.send(
                            '''
                            Creating new playlist
                            ``{0}`` and adding ``{1}`` to the list.
                            '''
                            .format(content[2], content[3])
                        )
                elif content[1].startswith('del'):
                    return await message.channel.send(
                        'Removing ``{0}`` from playlist ``{1}``'
                        .format(content[3], content[2])
                    )
                elif content[1].startswith('play'):
                    return await message.channel.send(
                        'Playing {0}'.format(content[2])
                    )
                else:
                    return await message.channel.send(usage)
            elif content[0].startswith('play'):
                await play_song(message, int(content[1]))
            elif content[0].startswith('fetch'):
                if content[1].startswith('https://www.youtube.com/watch?v='):
                    await fetch_song(message, content[1])
                else:
                    return await message.channel.send(
                        "must contain valid youtube url"
                    )
            elif content[0].startswith('list'):
                if content[1].startswith('all'):
                    songs = await list_all_songs()
                    stitle = '\n'.join([
                        '(' + str(song['id']) + ') - ' +
                        str(song['title']) for song in songs
                    ])

                    await message.channel.send(
                        '''```{0}```'''.format(
                            stitle
                        )
                    )
            else:
                return await message.channel.send(usage)
        else:
            return await message.channel.send(usage)
