import requests
from src import parameters

r = requests.post(parameters.KODI_HTTP_URL, json={"jsonrpc": "2.0", "id": 1, "method": "Player.Open", "params":
                 {"item": {"channelid": 147}}})
print(r.status_code, r.reason)
# 200 OK