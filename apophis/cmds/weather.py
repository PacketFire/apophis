from cmds.command import Command
import pyowm


class WeatherCommand(Command):
    async def handle(self, context, message) -> str:
        content = message.content[8:].split()

        if not content:
            return await message.channel.send(
                'usage: !weather <zip/place>'
                '<zipcode> <country> or place: <City,State,Country>'
            )

        else:
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

            elif len(content[0]) == 5 and content[0].isdigit():
                place = content[0]
                if len(content) == 2:
                    country = content[1]
                else:
                    country = 'US'

                observe = owm.weather_at_zip_code(place, country)

            elif not content[0].isdigit():
                place = message.content[9:]
                observe = owm.weather_at_place(place)

            weather = observe.get_weather()
            return await message.channel.send(
                'The current weather for {0}: '
                ':thermometer: temperature {1}˚F, :droplet: humidity {2}%, '
                ':wind_blowing_face: wind speed {3} mph. '
                'Conditions: {4}'
                .format(
                    place,
                    weather.get_temperature('fahrenheit')['temp'],
                    weather.get_humidity(),
                    weather.get_wind()['speed'],
                    weather.get_status()
                )
            )
