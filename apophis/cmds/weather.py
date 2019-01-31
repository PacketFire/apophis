from cmds.command import Command
import pyowm


class WeatherCommand(Command):
    async def handle(self, context, message) -> str:
        content = message.content[8:].split()

        if content[0] is not None:
            owm = pyowm.OWM(context['config']['weather_token'])
            if content[0] == 'zip':
                if len(content) == 3:
                    country = content[2]
                else:
                    country = 'US'

                observe = owm.weather_at_zip_code(content[1], country)
                weather = observe.get_weather()

                return await message.channel.send(
                    'The current weather for {0}: '
                    ':thermometer: temperature {1}˚F, :droplet: humidity {2}, '
                    ':wind_blowing_face: wind speed {3} mph.'
                    .format(
                        message.content[13:],
                        weather.get_temperature('fahrenheit')['temp'],
                        weather.get_humidity(),
                        weather.get_wind()['speed']
                    )
                )
            elif content[0] == 'place':
                observe = owm.weather_at_place(message.content[15:])
                weather = observe.get_weather()

                return await message.channel.send(
                    'The current weather for {0}: '
                    ':thermometer: temperature {1}˚F, :droplet: humidity {2}, '
                    ':wind_blowing_face: wind speed {3} mph.'
                    .format(
                        message.content[13:],
                        weather.get_temperature('fahrenheit')['temp'],
                        weather.get_humidity(),
                        weather.get_wind()['speed']
                    )
                )

        else:
            return await message.channel.send(
                '''
                usage: !weather <zip/place>
                zip: <code> <country> place: <City,State,Country>
                '''
            )
