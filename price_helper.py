import aiohttp


async def price(item_name):
    url = 'https://west.albion-online-data.com/api/v2/stats/Prices/' + item_name + '.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_data = await response.json()
            results = []
            for item in json_data:
                if 'city' in item and 'sell_price_min' in item and 'quality' in item:
                    city = item['city']
                    price = item['sell_price_min']
                    quality = item['quality']
                    if int(price) != 0:
                        results.append((city, price, quality))
            if results:
                return results
            else:
                return None


