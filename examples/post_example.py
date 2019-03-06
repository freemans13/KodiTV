import requests
r = requests.post("http://127.0.0.1:8080/jsonrpc", json={"jsonrpc": "2.0", "id": 1, "method": "Player.Open", "params":
                 {"item": {"channelid": 147}}})
print(r.status_code, r.reason)
# 200 OK