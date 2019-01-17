import json
from cmds.command import Command
from typing import NamedTuple
from pytube import YouTube
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


async def song_exists(link) -> bool:
    statement = 'select link from song where link = $1'
    db = await connect()
    song = await db.fetchrow(statement, link)
    await db.close()

    if song['link']:
        return True
    else:
        return False


async def play_song(message, title):
    if title.isdigit():
        statement = 'select title from songs where id = $1'
        db = await connect()
        song = await db.fetchrow(statement, int(title))
        voice = await message.author.voice.channel.connect()
        voice.play(FFmpegPCMAudio('data/music/' + song['title'] + '.mp4'))
        await db.close()
        return await message.channel.send(
            'Playing {0}'.format(song['title'])
        )
    else:
        voice = await message.author.voice.channel.connect()
        voice.play(FFmpegPCMAudio('data/music/' + title))
        return await message.channel.send(
            'Playing {0}'.format(title)
        )


async def fetch_song(message, link):
    if song_exists(link) is False:
        await message.channel.send(
            'Downloading {0}'.format(link)
        )

        YouTube(link).streams.first().download(
            'data/music/',
        )
        yt = YouTube(link)

        statement = '''
            insert into songs (
                title,
                userid,
                uploader,
                link,
                duration
            )
            values($1, $2, $3, $4, $5);
        '''

        db = await connect()
        await db.execute(
            statement,
            yt.title,
            str(message.author.id),
            message.author.name,
            link,
            int(yt.length),
        )
        await db.close()

        return await message.channel.send(
            '{0} Downloaded {1}'.format(
                message.author.name,
                yt.title
            )
        )
    else:
        return await message.channel.send(
            'That song already exists in the database.'
        )


class MusicCommand(Command):
    def __init__(self, cmd_data):
        self.cmd_data = cmd_data

    async def parse_command(self, message, vc):
        usage = "usage: #music playlist <add/del/play>"
        content = list(message.content[7:].split())

        if len(content) >= 2:
            if content[0].startswith('playlist'):
                if content[1].startswith('add'):
                    if playlist_file_exists(content[2]):
                        write_playlist_file(content[2], content[3])
                        return message.channel.send(
                            'Adding ``{0}`` to playlist ``{1}``'
                            .format(content[3], content[2])
                        )
                    else:
                        write_playlist_file(content[2], content[3])
                        return message.channel.send(
                            '''
                            Creating new playlist
                            ``{0}`` and adding ``{1}`` to the list.
                            '''
                            .format(content[2], content[3])
                        )
                elif content[1].startswith('del'):
                    return message.channel.send(
                        'Removing ``{0}`` from playlist ``{1}``'
                        .format(content[3], content[2])
                    )
                elif content[1].startswith('play'):
                    return message.channel.send(
                        'Playing {0}'.format(content[2])
                    )
                else:
                    return await message.channel.send(usage)
            elif content[0].startswith('play'):
                await play_song(message, content[1])
            elif content[0].startswith('fetch'):
                if content[1].startswith('https://www.youtube.com/watch?v='):
                    await fetch_song(message, content[1])
                else:
                    return await message.channel.send(
                        "must contain valid youtube url"
                    )
            elif content[0].startswith('list'):
                if content[1].startswith('all'):
                    db = await connect()
                    row = await db.fetch('''select * from songs''')
                    return await message.channel.send(
                        row
                    )
            else:
                return await message.channel.send(usage)
        else:
            return await message.channel.send(usage)
