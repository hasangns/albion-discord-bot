import requests

url = 'https://raw.githubusercontent.com/ao-data/ao-bin-dumps/master/formatted/items.json'

response = requests.get(url)
data = response.json()

for item in data:
    localized_names = item.get('LocalizedNames')
    if localized_names and 'EN-US' in localized_names:
        item_name = localized_names['EN-US']

        unique_name = item.get('UniqueName')
        if unique_name:
            print(item_name, unique_name)