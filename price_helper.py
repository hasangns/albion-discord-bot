import aiohttp
import asyncio


async def price(item_name):
    url = 'https://west.albion-online-data.com/api/v2/stats/Prices/' + item_name + '.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_data = await response.json()
            results = []
            for item in json_data:
                if 'item_id' in item and 'city' in item and 'sell_price_min' in item and 'quality' in item:
                    item_id = item['item_id']
                    city = item['city']
                    price = item['sell_price_min']
                    quality = item['quality']
                    results.append((item_id, city, price, quality))
            return results
