import requests

name = 'ZeusReis'
url = 'https://gameinfo.albiononline.com/api/gameinfo/search?q=' + name

json = requests.get(url).json()

name = json['players'][0]['Name']
killFame = json['players'][0]['KillFame']
deathFame = json['players'][0]['DeathFame']

#print(name,killFame,deathFame)