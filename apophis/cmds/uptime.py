""" Uptime Command """
import calendar
from datetime import timedelta
import time

from cmds.command import Command


class UptimeCommand(Command):
    async def handle(self, context, message):
        start_time = context['start_time']
        current_time = calendar.timegm(time.gmtime())
        elapsed = timedelta(seconds=current_time - start_time)

        duration = '{} days, {} hours, {} minutes, {} seconds'.format(
            elapsed.days,
            elapsed.seconds // 3600,
            (elapsed.seconds // 60) % 60,
            elapsed.seconds % 60
        )

        return await message.channel.send(
            'I have been running for {}.'.format(duration)
        )
