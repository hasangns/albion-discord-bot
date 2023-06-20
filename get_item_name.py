import requests
import difflib

url = 'https://raw.githubusercontent.com/ao-data/ao-bin-dumps/master/formatted/items.json'

response = requests.get(url)
data = response.json()


def item_id_finder(name):
    print(name)
    liste = name.split()
    matching_unique_names = difflib.get_close_matches(liste[0].upper() + "_" + liste[1].upper(), [item.get('UniqueName') for item in data], n=1, cutoff=0.4)
    if matching_unique_names:
        matching_unique_name = matching_unique_names[0]
        for item in data:
            if item.get('UniqueName') == matching_unique_name:
                pass
        return matching_unique_name
    else:
        return None

def item_name_finder(name):
    list = name.split()
    matching_unique_names = difflib.get_close_matches(list[0].upper() + "_" + list[1].upper(), [item.get('UniqueName') for item in data], n=1,cutoff=0.6)
    if matching_unique_names:
        matching_unique_name = matching_unique_names[0]
        for item in data:
            if item.get('UniqueName') == matching_unique_name:
                localized_names = item.get('LocalizedNames')
                if localized_names and 'EN-US' in localized_names:
                    item_name = localized_names['EN-US']
                    break
        return item_name
    else:
        return None

