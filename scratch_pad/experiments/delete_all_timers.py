import requests
import json

r = requests.get('''http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","id":1,"method":"PVR.GetTimers"}''')
dict = r.json()

timers = []
for timerid in dict['result']['timers']:
    timers.append(timerid['timerid'])

for i in timers:
    r = requests.post('http://127.0.0.1:8080/jsonrpc',
                      json={"jsonrpc": "2.0", "id": 1, "method": "PVR.DeleteTimer", "params":
                          {"timerid": i}})
    print(r.text, r.status_code)
print("done")
print(len(timers))
