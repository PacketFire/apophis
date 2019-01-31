from cmds.command import Command
import pyowm


class WeatherCommand(Command):
    async def handle(self, context, message) -> str:
        content = message.content[8:].split()

        if content[0] is not None:
            owm = pyowm.OWM(context['config']['weather_token'])
            if content[0] == 'zip':
                place = content[1]
                if len(content) == 3:
                    country = content[2]
                else:
                    country = 'US'

                observe = owm.weather_at_zip_code(place, country)
            elif content[0] == 'place':
                place = message.content[15:]
                observe = owm.weather_at_place(place)

            weather = observe.get_weather()
            return await message.channel.send(
                'The current weather for {0}: '
                ':thermometer: temperature {1}˚F, :droplet: humidity {2}, '
                ':wind_blowing_face: wind speed {3} mph.'
                .format(
                    place,
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