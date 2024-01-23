import os

import discord
import re 
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')

LINK_PATTERN = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?(\/.*){0,}'



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    
    print(f'{client.user} has connected to the {guild.name} Discord server!')

    await find_new_links(guild)



@client.event
async def on_message(message):

    if message.author == client.user:
        return
        

    if re.search(LINK_PATTERN, message.content):
        target_channel = set_target_channel(message.guild, CHANNEL)

        if target_channel == message.channel:
            # if the message is in the channel we want to post to, ignore it
            return
        
        await target_channel.send(link_message_builder(message))


    if message.content == 'hello':
        await message.channel.send('hello')


async def find_new_links(guild):
    target_channel = discord.utils.get(guild.channels, name=CHANNEL)

    unchecked_channels = [guild for guild in guild.text_channels if guild != target_channel]
    new_links = []
    links_in_correct_channel = []

    async for message in target_channel.history(limit=200):
        if re.search(LINK_PATTERN, message.content):
            links_in_correct_channel.append(re.search(LINK_PATTERN, message.content).group())
    if links_in_correct_channel:
        print(f'got all links in {target_channel}')


    for channel in unchecked_channels:
        print(f'checking {channel}')
        async for message in channel.history(limit=200):
            if re.search(LINK_PATTERN, message.content) and re.search(LINK_PATTERN, message.content).group() not in links_in_correct_channel:
                print(f'new link found: {re.search(LINK_PATTERN, message.content).group()}')
                new_links.append(link_message_builder(message))

    
    # if new_links:
    #     print(f'new links found: {new_links}')
    #     await target_channel.send(new_links)


def set_target_channel(guild, channel):
    return discord.utils.get(guild.channels, name=channel)

def link_message_builder(message):
    link = re.search(LINK_PATTERN, message.content).group()
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

    return f'Website: {name.title()}\n{link}'

client.run(TOKEN)
