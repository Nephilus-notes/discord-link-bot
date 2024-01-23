import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    
    print(
        f'{client.user} is connected to the following guild: \n'
        f'{guild.name} (id: {guild.id})'
    )
    print(f'{client.user} has connected to Discord!')

    channels = '\n - '.join([channel.name for channel in guild.channels])
    print(f'Guild Channels: \n - {channels}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'hello':
        await message.channel.send('hello')

client.run(TOKEN)
