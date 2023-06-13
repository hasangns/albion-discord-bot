import aiohttp


async def price(item_name):
    url = 'https://west.albion-online-data.com/api/v2/stats/Prices/' + item_name + '.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_data = await response.json()
            results = []
            for item in json_data:
                if 'city' in item and 'sell_price_min' in item and 'quality' in item:  # Check items if it is in item
                    city = item['city']
                    price = item['sell_price_min']
                    quality = item['quality']

                    if quality == 1:
                        new_quality = "Normal"
                    elif quality == 2:
                        new_quality = "Good"
                    elif quality == 3:
                        new_quality = "Outstanding"
                    elif quality == 4:
                        new_quality = "Excellent"
                    else:
                        new_quality = "Masterpiece"

                    if int(price) != 0:
                        # Append all in
                        results.append((city, price, new_quality))
            if results:  # If it is not none return
                return results
            else:
                return None
