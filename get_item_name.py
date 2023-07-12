import requests
import difflib


url = 'https://raw.githubusercontent.com/ao-data/ao-bin-dumps/master/formatted/items.json'

response = requests.get(url)
data = response.json()


def item_id_finder(name):
    matches = difflib.get_close_matches(name, [item.get('LocalizedNames', {}).get(
        'EN-US') for item in data if item.get('LocalizedNames')], n=1, cutoff=0.6)
    if matches:
        matching_name = matches[0]
        for item in data:
            localized_names = item.get('LocalizedNames')
            if localized_names and localized_names.get('EN-US') == matching_name:
                unique_name = item.get('UniqueName')
                return unique_name


def item_name_finder(name):
    matches = difflib.get_close_matches(name, [item.get('LocalizedNames', {}).get(
        'EN-US') for item in data if item.get('LocalizedNames')], n=1, cutoff=0.6)
    if matches:
        matching_name = matches[0]
        for item in data:
            localized_names = item.get('LocalizedNames')
            if localized_names and localized_names.get('EN-US') == matching_name:
                item_name = localized_names['EN-US']
                return item_name