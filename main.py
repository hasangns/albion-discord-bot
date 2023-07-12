import os
import discord
import configparser
from datetime import datetime
from price_helper import check_price, check_profit
from get_item_name import item_name_finder, item_id_finder


# Tiers
tiers = {
    't2': "Novice's",
    't3': "Journeyman's",
    't4': "Adept's",
    't5': "Expert's",
    't6': "Master's",
    't7': "Grandmaster's",
    't8': "Elder's"
}


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


# Logging message
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
        item_tier = split[1]
        item_tier = item_tier.lower()
        item_tier = tiers.get(item_tier, item_tier)
        item_name = split[2]

        total = item_tier + " " + item_name
        item_id = item_id_finder(total)

        results = await check_price(item_id_finder(total))
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
                title=f"Price Of {item_name_finder(total)}",
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
            embed.set_thumbnail(
                url="https://render.albiononline.com/v1/item/" + item_id
            )
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("Item price not found")

    if message.content.startswith("!arbitrage"):
        split = user_message.split()
        if len(split) > 2 and len(split) < 5:
            item_tier = split[1]
            item_tier_old = split[1]
            item_tier = item_tier.lower()
            item_tier = tiers.get(item_tier, item_tier)
            item_name = split[2]

            total = item_tier + " " + item_name
            item_id = item_id_finder(total)

            results = await check_profit(item_id)
            if results is not None:
                blackMarket = "\n".join(
                    f"{bm_price} - {qualities}"
                    for bm_price, _, _, qualities, _, _, bm_date, _ in results
                )
                otherCities = "\n".join(
                    f"{others_city} - {others_price} - {qualities}"
                    for _, others_price, others_city, qualities, _, _, _, others_date in results
                )
                profit = "\n".join(
                    f" {str(profit)}"
                    for _, _, _, _, profit, preProfit, _, _ in results
                )

                # If you want to check uptade date you can unlock
                blackMarketDate = "\n".join(
                    f"{datetime.strptime(bm_date, '%Y-%m-%dT%H:%M:%S')}"
                    for _, _, _, _, _, _, bm_date, _ in results
                )
                otherCitiesDate = "\n".join(
                    f"{others_city} - {datetime.strptime(others_date, '%Y-%m-%dT%H:%M:%S')}"
                    for _, _, others_city, _, _, _, _, others_date in results
                )

                embed = discord.Embed(
                    title=f"Arbitrage Of {item_name_finder(total)}",
                )
                embed.add_field(
                    name="Black Market Price", value=blackMarket, inline=True
                )
                embed.add_field(
                    name="Other Cities Price", value=otherCities, inline=True
                )
                embed.add_field(
                    name="Profit", value=profit, inline=True
                )
                try:
                    embed.add_field(
                        name="Black Market Amount", value=open(str(item_tier_old) + str(item_name),"r").read(), inline=False
                    )
                except:
                    embed.add_field(
                        name="Black Market Amount", value="Not defined", inline=False
                    )
                embed.set_thumbnail(
                    url="https://render.albiononline.com/v1/item/" + item_id
                )


                # If you want to check uptade date you can unlock
                """embed.add_field(
                    name="Black Market Last Uptade", value=blackMarketDate, inline=True
                )"""
                """embed.add_field(
                    name="Other Cities Last Uptade", value=otherCitiesDate, inline=True
                )"""
                embed.set_footer(
                    text="This results are from albion online data. It is not provide live data"
                )

                await message.channel.send(embed=embed)
            else:
                await message.channel.send("Item is not profitable")
        else:
            await message.author.send("This is a wrong usage you can use like this:\n!arbitrage t4 leather")

    if message.content.startswith("!add"):
        split = user_message.split()
        item_tier = split[1]
        item_name = split[2]
        item_quality = split[3]
        item_amount = split[4]

    if message.content.startswith("!add"):
        split = user_message.split()
        item_tier = split[1]
        item_name = split[2]
        item_quality = split[3]
        item_amount = split[4]

        with open(str(item_tier) + str(item_name),"a") as appendfile:
            appendfile.write(item_tier + " " + item_name + " " + item_quality + " " + item_amount + "\n")
            appendfile.close()


client.run(discord_token)