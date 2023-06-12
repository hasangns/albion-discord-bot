import os
import discord
import configparser
from price_helper import price


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
    name="Albion"), intents=intents)


@client.event
async def on_ready():
    print("Bot has logged in as {0.user}".format(client))


@client.event
async def on_message(message):

    user = str(message.author.name)

    user_message = str(message.content)
    channel = str(message.channel)

    print(user + ":" + " " + user_message +
          " " + "at" + " " + channel.capitalize())

    if message.author == client.user:
        return

    if message.content.startswith('!price'):
        item_name = user_message[7:]
        if item_name == "":
            await message.channel.send("Item is not exist")
        else:
            embed = discord.Embed(title=f"Price of {item_name}", url='https://github.com/iamgunes', description=await price(item_name))
            embed.add_field(name="Item Name", value="> Test 1", inline=True)
            embed.add_field(name="City", value="> Test 2", inline=True)
            embed.add_field(name="Price", value="> Test 3", inline=True)
            #embed.add_field(name="Quality", value="> Test 4", inline=True)
            await message.channel.send(embed=embed)


client.run(discord_token)
