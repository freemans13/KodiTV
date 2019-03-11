import requests
import json
import parameters

def play_something():
    response = requests.get(parameters.KODI_HTTP_URL + '''?request={"jsonrpc":"2.0","id":1,"method":"PVR.GetRecordings"}''')
    record_dict = json.loads(response.text)

    # for recording in record_dict['result']['recordings']:

    rec_to_post = record_dict['result']['recordings'][0]['recordingid']

    r = requests.post(parameters.KODI_HTTP_URL,
                      json={"jsonrpc": "2.0", "id": 1,
                            "method": "Player.Open",
                            "params": {"item": {"recordingid": rec_to_post}}})


