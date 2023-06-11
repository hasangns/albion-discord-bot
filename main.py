import os
import discord
import aiohttp
import configparser


# Load config.ini
currentPath = os.path.dirname(os.path.realpath(__file__))
configs = configparser.ConfigParser()
configs.read(currentPath + "/config.ini")

discord_token = configs["TOKEN"]['botToken']

# Command Prefix


# Set up logging to discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(status='Online', activity=discord.Game(
    name="Albion"), intents=intents, command_prefix='!')


@client.event
async def on_ready():
    print("Bot has logged in as {0.user}".format(client))

@client.event
async def on_message(message):

    user = str(message.author.name)
    user_message = str(message.content)
    channel = str(message.channel)

    print(user + ":" + " " + user_message + " " + "at" + " " + channel.capitalize())

    if message.author == client.user:
        return

    if message.content.startswith('!price'):
        item_name = user_message[7:]
        url = 'https://west.albion-online-data.com/api/v2/stats/Prices/' + item_name + '.json'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                json = await response.json()
                for i in range(len(json)):
                    item = json[i]['item_id']
                    city = json[i]['city']
                    price = json[i]['sell_price_min']
                    quality = json[i]['quality']
                    total = item + ' ' + city + ' ' + str(price) + ' ' + str(quality)
                    #print(total)
                    if (int(price) != 0):
                        embed = discord.Embed(title='Prices of' + item_name,description=price)
                        await message.channel.send(embed=embed)


client.run(discord_token)
