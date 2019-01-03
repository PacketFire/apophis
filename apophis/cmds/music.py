import json
from cmds.command import Command
from typing import NamedTuple
from pytube import YouTube
from discord import FFmpegPCMAudio


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
        with open('data/music/' + filename + '.json', 'a+') as fh:
            fh.write(json.dumps(file_data))


def playlist_file_exists(filename: str) -> bool:
    try:
        fh = open('data/music/' + filename + '.json', 'r')
        fh.close()
        return True
    except IOError:
        return False


class MusicCommand(Command):
    def __init__(self, cmd_data):
        self.cmd_data = cmd_data

    async def parse_command(self, message, vc):
        usage = "usage: #music playlist <add/del/play>"
        content = message.content[7:].split(
            " ",
            message.content[7:].count(" ")
        )

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
                            'Creating new playlist ``{0}`` and adding ``{1}`` to the list.'
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
                    return message.channel.send(usage)
            elif content[0].startswith('play'):
                voice = await message.author.voice.channel.connect()
                voice.play(FFmpegPCMAudio('data/music/' + content[1]))
                return await message.channel.send(
                    'Playing {0}'.format(content[1])
                )
            elif content[0].startswith('fetch'):
                if content[1].startswith('https://www.youtube.com/watch?v='):
                    await message.channel.send(
                        'Downloading {0}'.format(content[1])
                    )

                    YouTube(content[1]).streams.first().download(
                        'data/music/', filename=content[2]
                    )

                    return await message.channel.send(
                        'Downloaded {0}'.format(content[1])
                    )
            else:
                return message.channel.send(usage)
        else:
            return message.channel.send(usage)
