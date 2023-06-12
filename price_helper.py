import aiohttp


async def price(item_name):
    list = []
    url = 'https://west.albion-online-data.com/api/v2/stats/Prices/' + item_name + '.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json = await response.json()
            for i in range(len(json)):
                item = json[i]['item_id']
                city = json[i]['city']
                price = json[i]['sell_price_min']
                quality = json[i]['quality']
                total = item + ' ' + city + ' ' + \
                    str(price) + ' ' + str(quality)
                if (int(price) != 0):
                    list.append(total)
            join = "\n".join(list)
            return list
