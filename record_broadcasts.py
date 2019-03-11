import requests
import json
from read_logs import read_logs
import parameters


def add_timer(title, broadcast_id):
    r = requests.get(parameters.KODI_HTTP_URL + '''?request=
                       {"jsonrpc":"2.0","id":1,"method":"PVR.GetTimers","params":{"properties":[]}}''')
    response = r.text
    timers = json.loads(response)

    new_timer = True
    for timer in timers['result']['timers']:
        timer_title = timer['label']
        if title == timer_title:
            new_timer = False
            break

    if new_timer:
        print(broadcast_id)
        r = requests.post(parameters.KODI_HTTP_URL,
                          json={"jsonrpc": "2.0", "id": 1,
                                "method": "PVR.AddTimer",
                                "params": {"broadcastid": broadcast_id, "timerrule": True}})
        print(r.status_code, r.reason)


def processor(connection, cursor, log_dict):
    print(log_dict['event']['method'])
    if log_dict['event']['method'] == "Player.OnAVChange":
        print("TV show has started")
        print(log_dict)
        tv_show = True
        try:
            if log_dict['event']['params']['data']['type'] == "channel":
                pass
            else:
                tv_show = False
        except KeyError:
            if log_dict['event']['params']['data']['item']['type'] == "channel":
                pass
            else:
                tv_show = False

        if tv_show:
            channelnumber = log_dict['event']['params']['data']['item']['id']
            print(str(channelnumber))
            # print('''{"jsonrpc":"2.0","id":1,"method":"PVR.GetChannelDetails","params":{"channelid":''' + str(channelnumber) + ''',"properties": ["broadcastnow"]}}''')

            r = requests.get(
                parameters.KODI_HTTP_URL + '''?request=
                {"jsonrpc":"2.0","id":1,"method":"PVR.GetChannelDetails","params":{"channelid":'''
                + str(channelnumber) + ''',"properties": ["broadcastnow"]}}''')

            if r.status_code == 200:
                broadcast_details = r.text
                print(r.text)
                broadcastdetails_json = json.loads(broadcast_details)
                print(broadcastdetails_json)
                if 'result' not in broadcastdetails_json or 'broadcastnow' not in broadcastdetails_json:
                    #this is an old record. Skip it
                    pass
                else:
                    title = broadcastdetails_json['result']['channeldetails']['broadcastnow']['title']
                    broadcastid = broadcastdetails_json['result']['channeldetails']['broadcastnow']['broadcastid']

                    add_timer(title, broadcastid)

read_logs(processor)
