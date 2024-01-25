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



 # When a new message is posted in the server, check if it's a link, and then repost it in the links channel
@client.event
async def on_message(message):

    if message.author == client.user:
        return
        

    if re.search(LINK_PATTERN, message.content):
        # institute a findall method to grab all links in a message
        # then iterate through the list and send each one individually
        # await message.channel.send(link_message_builder(message))
        target_channel = set_target_channel(message.guild, CHANNEL)

        if target_channel == message.channel:
            # if the message is in the channel we want to post to, ignore it
            return
  
        async for post in target_channel.history(limit=200):
            if link_message_builder(message) in post.content:

                print('link already posted')
                return

        
        await target_channel.send(link_message_builder(message))


    if message.content == 'hello':
        await message.channel.send('hello')


async def find_new_links(guild):
    target_channel = discord.utils.get(guild.channels, name=CHANNEL)

    unchecked_channels = [guild for guild in guild.text_channels if guild != target_channel]
    new_links = set()
    links_in_correct_channel = set()

    # getting all the links in the target channel
    async for message in target_channel.history(limit=200):
        if re.search(LINK_PATTERN, message.content):

            # attempting to split the message into a list of links if necessary
            uncleaned_link = re.search(LINK_PATTERN, message.content).group()
                #  adding the link to the set of links or splitting it into multiple links theoretically
            if whitespace_check(uncleaned_link):
                multi_link_split(uncleaned_link, new_links, links_in_correct_channel, False)
            else:
                links_in_correct_channel.add(uncleaned_link)

    # getting all the links in the other channels and checking it against the
    # links in the target channel before adding them to the new_links set
    for channel in unchecked_channels:
        async for message in channel.history(limit=200):
            if re.search(LINK_PATTERN, message.content):
                link = re.search(LINK_PATTERN, message.content).group()
                if link in links_in_correct_channel or link in new_links:
                    continue
                else:
                    if whitespace_check(link):
                        multi_link_split(link, new_links, links_in_correct_channel)
                    else:
                        new_links.add(link_message_builder(message))

    # sending the new links to the target channel
    if new_links:
        for link in new_links:
            await target_channel.send(link)


def set_target_channel(guild, channel):
    return discord.utils.get(guild.channels, name=channel)

def link_message_builder(message, string_boolean=False):
    name = site_name_extractor(message) if string_boolean else site_name_extractor(message.content)
    link = message if string_boolean else re.search(LINK_PATTERN, message.content).group()

    return f'Website: {name.title()} \n {link}'


async def delete_awkward_links(guild, channel):
    target_channel = set_target_channel(guild, channel)
    async for message in target_channel.history(limit=200):
        if link_pattern_match(message):
            regex_match = re.search(LINK_PATTERN, message.content).group()
            if ' ' in regex_match:
                await message.delete()
            if type(regex_match) == str:
                continue
            elif type (regex_match) == list:
                print("it's a list")

def link_pattern_match(message):
    if re.search(LINK_PATTERN, message.content):
        return True
    else:
        return False
    
def multi_link_split(link, new_links_set, links_in_correct_channel, push_boolean=True):
    multiple_links = link.split(' ')
    for link in multiple_links:
        if link not in links_in_correct_channel:
            if push_boolean:
                new_links_set.add(link_message_builder(link, True))
            else:
                links_in_correct_channel.add(link)

def site_name_extractor(link):

    https_follow_up = re.search(r'(?<=https:\/\/)[a-zA-Z0-9]{2,}', link)
    # print(https_follow_up)
    if https_follow_up:
        https_follow_up = https_follow_up.group()
    else:
        return 'No name found'
    #     https_follow_up = re.search(r'(?<=http:\/\/)[a-zA-Z0-9]{2,}', link).group()
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

def whitespace_check(link):
    if ' ' in link:
        return False
    else:
        return True

client.run(TOKEN)
