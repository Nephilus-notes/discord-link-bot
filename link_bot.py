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

    # await delete_awkward_links(guild, CHANNEL)

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
    new_links = set()
    links_in_correct_channel = set()

    async for message in target_channel.history(limit=200):
        if re.search(LINK_PATTERN, message.content):
            # print(f'link found in channel: {re.search(LINK_PATTERN, message.content).group()}')
            links_in_correct_channel.add(re.search(LINK_PATTERN, message.content).group())
    # if links_in_correct_channel:
    #     print(f'got all links in {links_in_correct_channel}')


    for channel in unchecked_channels:
        # print(f'checking {channel}')
        async for message in channel.history(limit=200):
            if re.search(LINK_PATTERN, message.content):
                link = re.search(LINK_PATTERN, message.content).group()
                if link in links_in_correct_channel or link in new_links:
                    # print(f'link already in channel: {link}')
                    continue
                else:
                    if ' ' in link:
                        # continue
                        multi_link_split(link, new_links)
                    else:
                        new_links.add(link_message_builder(message))

    
    # print('links in channel: ')
    # for link in links_in_correct_channel:
    #     print(link)
    if new_links:

        # print(links_in_correct_channel, new_links)
        # print(f'new links found: {new_links}\n')
        for link in new_links:
            await target_channel.send(link)
        # await target_channel.send(new_links)


def set_target_channel(guild, channel):
    return discord.utils.get(guild.channels, name=channel)

def link_message_builder(message, string_boolean=False):
    if string_boolean:
        return f'Website: {site_name_extractor(message)} \n {message}'
    else:
        link = re.search(LINK_PATTERN, message.content).group()
        name = site_name_extractor(link)

        return f'Website: {name.title()} \n {link}'


async def delete_awkward_links(guild, channel):
    target_channel = set_target_channel(guild, channel)
    async for message in target_channel.history(limit=200):
        if link_pattern_match(message):
            regex_match = re.search(LINK_PATTERN, message.content).group()
            # whitespace_check = re.search(r'(?<=https:\/\/)[a-zA-Z0-9]{2,}', message.content).group()
            if ' ' in regex_match:
                # print('whitespace detected')
                # print(regex_match)
                await message.delete()
            if type(regex_match) == str:
                continue
            elif type (regex_match) == list:
                print("it's a list")
            # print(f'link found in channel: {re.search(LINK_PATTERN, message.content).group()}')

def link_pattern_match(message):
    if re.search(LINK_PATTERN, message.content):
        return True
    else:
        return False
    
def multi_link_split(link, new_links_set):
    if ' ' in link:
        multiple_links = link.split(' ')
        for link in multiple_links:
            new_links_set.add(link_message_builder(link, True))

def site_name_extractor(link):
    https_follow_up = re.search(r'(?<=https:\/\/)[a-zA-Z0-9]{2,}', link).group()
    # grab the first part of the url so the switch can determine where to grab the name from

    name = ''
    match https_follow_up:
        case 'docs':
            # print('docs detected')
            name = re.search(r'(?<=docs.)[a-zA-Z0-9]{2,}', link).group()
        case 'www':
            # print('www detected')
            name = re.search(r'(?<=www.)[a-zA-Z0-9]{2,}', link).group()
        case _:
            # print('nothing specific detected')
            name = re.search(r'(?<=https://)[a-zA-Z0-9]{2,}', link).group() # https regex
                
    return name.title()

client.run(TOKEN)
