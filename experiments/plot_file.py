import requests
import parameters
import json


r = requests.get(parameters.KODI_HTTP_URL + '''?request={"jsonrpc":"2.0","id":1,"method":"PVR.GetChannels","params":{
"channelgroupid":"alltv"}}''')

response = r.text
channels = json.loads(response)
for channel in channels['result']['channels']:
    channel_number = channel['channelid']

    r = requests.get( parameters.KODI_HTTP_URL + '''?request={"jsonrpc":"2.0","id":1,"method":"PVR.GetBroadcasts","params":{
        "channelid":''' + str(channel_number) + ''',"properties":[
        "title",
        "plot",
        "episodename",      
        "episodenum",
        "isseries"
        ]}}''')

    if r.status_code == 200:
        broadcast_details = r.text
        print(r.text)
        broadcast_details_json = json.loads(broadcast_details)
        for broadcast in broadcast_details_json['result']['broadcasts']:
            print(broadcast['plot'])


