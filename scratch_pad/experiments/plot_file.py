import requests
from src import parameters
import json


r = requests.get(parameters.KODI_HTTP_URL + '''?request={"jsonrpc":"2.0","id":1,"method":"PVR.GetChannels","params":{
"channelgroupid":"alltv"}}''')

channels = r.json()
for channel in channels['result']['channels']:
    channel_number = channel['channelid']

    r = requests.get(parameters.KODI_HTTP_URL + '''?request={"jsonrpc":"2.0","id":1,"method":"PVR.GetBroadcasts","params":{
        "channelid":''' + str(channel_number) + ''',"properties":[
        "title",
        "plot",
        "episodename",      
        "episodenum",
        "isseries"
        ]}}''')

    if r.status_code == 200:
        print(r.text)
        broadcast_details_json = r.json()
        for broadcast in broadcast_details_json['result']['broadcasts']:
            print(broadcast['plot'])


