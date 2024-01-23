import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()

# client = discord.Client(intents=intents)

class LinkBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'hello':
            await message.channel.send('Hello!')


# @client.event
# async def on_ready():
#     guild = discord.utils.get(client.guilds, name=GUILD)
    
#     print(
#         f'{client.user} is connected to the following guild: \n'
#         f'{guild.name} (id: {guild.id})'
#     )
    # print(f'{client.user} has connected to Discord!')
client = LinkBotClient(intents=intents)
client.run(TOKEN)
