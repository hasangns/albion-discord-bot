import os
import discord
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

    if message.author == client.author:
        return


client.run(discord_token)
