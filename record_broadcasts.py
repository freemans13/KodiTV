import requests
import os
from pygtail import Pygtail
import time
import json
txt_files = []
file_name = ""


while True:
    if len(txt_files) == 0:
        # see https://stackoverflow.com/questions/5640630/array-filter-in-python
        txt_files = [entry for entry in os.listdir("event_logs/") if entry.endswith('.txt')]
        txt_files.sort()
        if file_name != "":
            # we know the last file_name we processed - no point re-loading older files
            txt_files = [file for file in txt_files if file > file_name]
    if len(txt_files) > 0:
        # grab oldest file in the array (first element) and remove it from the array
        file_name = txt_files.pop(0)
    if file_name == "":
        time.sleep(1)
    else:

        current_programme_id = 0
        for line in Pygtail("event_logs/" + file_name, offset_file="event_logs/" + file_name + "." + os.path.basename(__file__) + ".offset"):
            log_dict = json.loads(line)
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
                except KeyError as e:
                    if log_dict['event']['params']['data']['item']['type'] == "channel":
                        pass
                    else:
                        tv_show = False

                if tv_show:
                    channelnumber = log_dict['event']['params']['data']['item']['id']
                    print(str(channelnumber))
                    # print('''{"jsonrpc":"2.0","id":1,"method":"PVR.GetChannelDetails","params":{"channelid":''' + str(channelnumber) + ''',"properties": ["broadcastnow"]}}''')

                    r = requests.get(
                        '''http://127.0.0.1:8080/jsonrpc?request=
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
                            broadcastid = broadcastdetails_json['result']['channeldetails']['broadcastnow']['broadcastid']

                            r = requests.get('''http://127.0.0.1:8080/jsonrpc?request=
                            {"jsonrpc":"2.0","id":1,"method":"PVR.GetTimers","params":{"properties":[]}}''')
                            response = r.text
                            timers = json.loads(response)

                            new_timer = True
                            title = broadcastdetails_json['result']['channeldetails']['broadcastnow']['title']
                            for timer in timers['result']['timers']:
                                timer_title = timer['label']
                                if title == timer_title:
                                    new_timer = False
                                    break

                            if new_timer:
                                print(broadcastid)
                                r = requests.post("http://127.0.0.1:8080/jsonrpc",
                                                  json={"jsonrpc": "2.0", "id": 1,
                                                        "method": "PVR.AddTimer",
                                                        "params": {"broadcastid": broadcastid, "timerrule": True}})
                                print(r.status_code, r.reason)


# 200 Ok
    time.sleep(5)
