from src.utils.read_logs import read_logs
import os
from src.utils.timer import add_timer
from src.utils.KodiResource import KodiResource


def processor(connection, cursor, log_dict):
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
            channel_id = log_dict['event']['params']['data']['item']['id']
            print("channel_id", str(channel_id))

            kodi = KodiResource()
            broadcastdetails_json = kodi.pvr_get_channel_details(channel_id)
            print("response for get channel details", broadcastdetails_json)
            if not broadcastdetails_json:
                # this is an old record. Skip it
                print("skip")
                pass
            elif 'broadcastnow' not in broadcastdetails_json:
                # this is an old record. Skip it
                print("skip")
                pass
            else:
                title = broadcastdetails_json['broadcastnow']['title']
                broadcast_id = broadcastdetails_json['broadcastnow']['broadcastid']

                add_timer(title, broadcast_id, kodi)


read_logs(processor, os.path.basename(__file__))
