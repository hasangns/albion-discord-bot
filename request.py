import asyncio
import aiohttp


async def price(item_name):
    url = 'https://west.albion-online-data.com/api/v2/stats/Prices/' + item_name + '.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json = await response.json()
            for i in range(len(json)):
                item = json[i]['item_id']
                city = json[i]['city']
                price = json[i]['sell_price_min']
                quality = json[i]['quality']
                if (int(price) != 0):
                    print(item, city, price, quality)

asyncio.run(price("T4_LEATHER"))
