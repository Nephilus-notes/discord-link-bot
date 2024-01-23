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
    
    print(f'{client.user} has connected to the {guild.name} Discord server!')



@client.event
async def on_message(message):

    if message.author == client.user:
        return
        
    pattern = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?(\/.*){0,}'
    # pattern to match a full url 
    if re.search(pattern, message.content):
        channel_target = discord.utils.get(message.guild.channels, name=CHANNEL)
        if channel_target == message.channel:
            # if the message is in the channel we want to post to, ignore it
            return
        
        link = re.search(pattern, message.content).group()
        https_follow_up = re.search(r'(?<=https:\/\/)[a-zA-Z0-9]{2,}', message.content).group()
        # grab the first part of the url so the switch can determine where to grab the name from
  
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

        # post the link with the name of the website to the channel
        await channel_target.send(f'Website: {name.title()}\n{link}')


    if message.content == 'hello':
        await message.channel.send('hello')

client.run(TOKEN)
