from cmds.command import Command
import pyowm


class WeatherCommand(Command):
    async def handle(self, context, message) -> str:
        content = message.content[8:].split()

        if content[0] is not None:
            owm = pyowm.OWM(context['config']['weather_token'])
            observe = owm.weather_at_place(message.content[9:])
            weather = observe.get_weather()

            return await message.channel.send(
                'The current weather for {0}: '
                ':thermometer: temperature {1}˚F, :droplet: humidity {2}, '
                ':wind_blowing_face: wind speed {3} mph.'
                .format(
                    message.content[9:],
                    weather.get_temperature('fahrenheit')['temp'],
                    weather.get_humidity(),
                    weather.get_wind()['speed']
                )
            )
        else:
            return await message.channel.send(
                'usage: !weather <City,State,Country>'
            )
