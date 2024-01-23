import os

import discord
import re 
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    
    print(
        f'{client.user} is connected to the following guild: \n'
        f'{guild.name} (id: {guild.id})'
    )
    print(f'{client.user} has connected to Discord!')

    # channels = '\n - '.join([channel.name for channel in guild.text_channels])
    # print(f'Guild Channels: \n - {channels}')

    # pattern = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?'
    # print(pattern)



@client.event
async def on_message(message):

    if message.author == client.user:
        return
    
    # print(f'messenger not bot. message: {message}')
    
    # pattern = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?'
    pattern = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?(\/.*){0,}'
    # print(pattern)

    if re.search(pattern, message.content):
        channel_target = discord.utils.get(message.guild.channels, name=CHANNEL)
        if channel_target == message.channel:
            return
        
        link = re.search(pattern, message.content).group()
        https_follow_up = re.search(r'(?<=https:\/\/)[a-zA-Z0-9]{2,}', message.content).group()
        # print(type(https_follow_up))
        # print(https_follow_up)
        name = ''
        match https_follow_up:
            case 'docs':
                print('docs detected')
                name = re.search(r'(?<=docs.)[a-zA-Z0-9]{2,}', message.content).group()
            case 'www':
                print('www detected')
                name = re.search(r'(?<=www.)[a-zA-Z0-9]{2,}', message.content).group()
            case _:
                print('nothing specific detected')
                name = re.search(r'(?<=https://)[a-zA-Z0-9]{2,}', message.content).group() # https regex


        # if not name:
        #     name = re.search(r'(?<=https://)[a-zA-Z0-9]{2,}', message.content).group() # https regex
        #     if name == 'docs':
        #         name = re.search(r'(?<=docs.)[a-zA-Z0-9]{2,}', message.content).group()
        # if not name or name in ['docs', 'www', 'http']:
        #     name = "bot name regex failed"


        # print('link detected')
        await channel_target.send(f'Website: {name.title()}\n{link}')


    if message.content == 'hello':
        await message.channel.send('hello')

client.run(TOKEN)
