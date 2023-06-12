import os
import discord
import configparser
from price_helper import price
from arbitrage_help import arbitrage


# Load config.ini
currentPath = os.path.dirname(os.path.realpath(__file__))
configs = configparser.ConfigParser()
configs.read(currentPath + "/config.ini")

discord_token = configs["TOKEN"]['botToken']

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
        split = user_message.split()
        item_name = split[1]
        results = await price(item_name)
        if results != None:
            n_city = ""
            n_price = ""
            n_quality = ""
            for city, item_price, quality in results:
                n_city += city + "\n"
                n_price += str(item_price) + "\n"
                n_quality += str(quality) + "\n"
            embed = discord.Embed(
                title=f"Price of {item_name}", url='https://github.com/iamgunes')
            embed.add_field(name="Location", value=n_city, inline=True)
            embed.add_field(name="Min Sell Price", value=n_price, inline=True)
            embed.add_field(name="Quality", value=n_quality, inline=True)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("Item price not found")

    if message.content.startswith('!arbitrage'):
        split = user_message.split()
        #item_tier = split[1]
        item_name = split[1]
        #item_quality = split[3]
        results = await arbitrage(item_name)
        if results != None:
            n_bm_city = ""
            n_others_city = ""
            n_profit = ""

            for bm_price, others_price, others_city, profit in results:
                #n_bm_price += str(bm_price) + "\n"
                n_bm_city += f" Black Market - {bm_price}\n"
                #n_others_price += str(others_price) + "\n"
                n_others_city += f"{others_city} - {others_price}\n"
                n_profit += str(profit) + "\n"
                print(others_city)
            embed = discord.Embed(
                title=f"Price of {item_name}", url='https://github.com/iamgunes')
            embed.add_field(name="Black Market Price", value=n_bm_city, inline=True)
            embed.add_field(name="Other Cities Price", value=n_others_city, inline=True)
            embed.add_field(name="Profit", value=n_profit, inline=True)

            await message.channel.send(embed=embed)
        else:
            await message.channel.send("Item is not profitable")


client.run(discord_token)
