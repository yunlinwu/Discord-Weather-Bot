import discord
import requests
import asyncio
import os

TOKEN = os.getenv('DISCORD_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
CHANNEL_ID = int(os.getenv('CHANNEL_ID')) 

intents = discord.Intents.default()

class WeatherBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)

    async def on_ready(self):
        self.bg_task = self.loop.create_task(self.send_weather())
        print(f'We have logged in as {self.user}')

    async def send_weather(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID)  # target channel ID

        while not self.is_closed():
            response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q=New%20York&appid={WEATHER_API_KEY}&units=metric')
            data = response.json()

            if response.status_code == 200:
                main = data['main']
                wind = data['wind']
                rain = data.get('rain', {'1h': 0})  # default to 0 if no data
                message = f"🌡️Temperature: {main['temp']}°C\n💨Wind Speed: {wind['speed']}m/s\n🌧️Rain: {rain['1h']}mm in the last hour\n🌫️Humidity: {main['humidity']}%\n☁️Pressure: {main['pressure']}hPa"
                await channel.send(message)
            else:
                await channel.send("Unable to get the weather at the moment.")

            await asyncio.sleep(3600)  # wait for an hour

client = WeatherBot()
client.run(TOKEN)
