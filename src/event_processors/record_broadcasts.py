import os
from src.utils.TimerManager import TimerManager
from src.utils.EventLogReader import EventLogReader
from src.utils.KodiResource import KodiResource


class RecordBroadcast(EventLogReader):

    def on_event(self, event_dict):
        if event_dict['event']['method'] == "Player.OnAVChange":
            print('---\n%s' % event_dict['event']['method'])
            tv_show = True
            try:
                if event_dict['event']['params']['data']['type'] == "channel":
                    pass
                else:
                    tv_show = False
            except KeyError:
                if event_dict['event']['params']['data']['item']['type'] == "channel":
                    pass
                else:
                    tv_show = False

            if tv_show:
                channel_id = event_dict['event']['params']['data']['item']['id']

                kodi = KodiResource()
                broadcastdetails_json = kodi.pvr_get_channel_details(channel_id)
                if not broadcastdetails_json:
                    # this is an old record. Skip it
                    print('Broadcast details not found. No Timer added')
                    pass
                elif 'broadcastnow' not in broadcastdetails_json:
                    # this is an old record. Skip it
                    print('Broadcast details not found. No Timer added')
                    pass
                else:
                    title = broadcastdetails_json['broadcastnow']['title']
                    broadcast_id = broadcastdetails_json['broadcastnow']['broadcastid']

                    TimerManager().add_timer(title, broadcast_id)


reader = RecordBroadcast(os.path.basename(__file__))
reader.start()
