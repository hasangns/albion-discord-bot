import aiohttp

qualities = {
    1: "Normal",
    2: "Good",
    3: "Outstanding",
    4: "Excellent",
    5: "Masterpiece"
}


async def check_price(item_name):
    url = f"https://west.albion-online-data.com/api/v2/stats/Prices/{item_name}.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_data = await response.json()
            results = []
            for item in json_data:
                if all(key in item for key in ('city', 'sell_price_min', 'quality')):
                    city = item['city']
                    price = item['sell_price_min']
                    quality = item['quality']

                    if int(price) != 0:
                        results.append((city, price, qualities.get(quality)))

            return results if results else None


async def check_profit(item_name):
    url = f"https://west.albion-online-data.com/api/v2/stats/Prices/{item_name}.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_data = await response.json()
            bm_data = []
            others_data = []
            results = []

            for item in json_data:
                if all(key in item for key in ('city', 'sell_price_min', 'sell_price_min_date', 'quality')):
                    city = item['city']
                    price = item['sell_price_min']
                    price_date = item['sell_price_min_date']
                    quality = item['quality']

                    if int(price) != 0:
                        if city == 'Black Market':
                            bm_data.append((price, quality, price_date))
                        else:
                            others_data.append(
                                (price, quality, city, price_date))

            for bm_price, bm_quality, bm_date in bm_data:
                for others_price, others_quality, others_city, others_date in others_data:
                    if bm_quality == others_quality and bm_price - others_price > 0:
                        profit = bm_price - \
                            int((bm_price * 0.08)) - others_price
                        preProfit = bm_price - \
                            int((bm_price * 0.04)) - others_price
                        if profit > 0:
                            results.append((bm_price, others_price, others_city, qualities.get(
                                bm_quality), profit, preProfit, bm_date, others_date))
                        else:
                            pass
            return results if results else None