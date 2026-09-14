import urllib.request
import json
req = urllib.request.Request("https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&generator=search&gsrsearch=golf%20course&gsrnamespace=0&gsrlimit=10&piprop=original&format=json", headers={'User-Agent': 'TeedUpBot/1.0'})
resp = urllib.request.urlopen(req)
print(json.loads(resp.read())['query']['pages'])
