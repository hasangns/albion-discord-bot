import os
import discord
import configparser
from price_helper import check_price, check_profit


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
        results = await check_price(item_name)
        if results is not None:
            location = "\n".join(
                f"{city}"
                for city, _, _, in results
            )
            sellPrice = "\n".join(
                f"{price}"
                for _, price, _, in results
            )
            qualities = "\n".join(
                f"{qualities}"
                for _, _, qualities in results
            )

            embed = discord.Embed(
                title=f"Price Of {item_name}",
                url='https://github.com/iamgunes'
            )
            embed.add_field(
                name="Location", value=location, inline=True
            )
            embed.add_field(
                name="Sell Price", value=sellPrice, inline=True
            )
            embed.add_field(
                name="Quality", value=qualities, inline=True
            )
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("Item price not found")

    if message.content.startswith("!arbitrage"):
        split = user_message.split()
        if len(split) > 2 and len(split) < 5:
            item_tier = split[1]
            item_name = split[2]
            results = await check_profit(item_tier, item_name)
            if results is not None:
                blackMarket = "\n".join(
                    f" Black Market - {bm_price} - {qualities} - {bm_date}"
                    for bm_price, _, _, qualities, _, bm_date, _ in results
                )
                otherCities = "\n".join(
                    f"{others_city} - {others_price} - {qualities} - {others_date}"
                    for _, others_price, others_city, qualities, _, _, others_date in results
                )
                profit = "\n".join(
                    str(profit) for _, _, _, _, profit, _, _ in results
                )

                embed = discord.Embed(
                    title=f"Arbitrage Of {item_name}",
                    url='https://github.com/iamgunes'
                )
                embed.add_field(
                    name="Black Market Price", value=blackMarket, inline=True
                )
                embed.add_field(
                    name="Other Cities Price", value=otherCities, inline=True
                )
                embed.add_field(name="Profit", value=profit, inline=True)

                await message.channel.send(embed=embed)
            else:
                await message.channel.send("Item is not profitable")
        else:
            await message.author.send("This is a wrong usage you can use like this:\n!arbitrage t4 leather")


client.run(discord_token)
