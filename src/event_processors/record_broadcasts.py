import os
from src.utils.TimerManager import TimerManager
from src.utils.EventLogReader import EventLogReader
from src.utils.KodiResource import KodiResource
from src.utils.DatabaseResource import DatabaseResource
from src.utils.Dislikes import Dislikes


class RecordBroadcast(EventLogReader):
    """
    Used to automatically add timers, if the show is being watched by the user
    """
    def __init__(self, offset_filename):
        super(RecordBroadcast, self).__init__(offset_filename)
        self.db = DatabaseResource()
        self.kodi = KodiResource()

    def on_event(self, event_dict):
        """
        If we get a Player.OnAvChange and the user is watching a live broadcast, and assuming  its not a disliked show,
        we add a timer.

        :param event_dict: Contains 3 elements; date, event, item
        :return: None
        """
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
                broadcastdetails_json = self.kodi.pvr_get_channel_details(channel_id)
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
                    dislikes = Dislikes(self.db.connection.cursor())
                    if not dislikes.is_disliked(title):
                        TimerManager().add_timer(title, broadcast_id)
                    else:
                        print("%s is a disliked show, no timer created" % title)
            else:
                print("This is not a live broadcast")


reader = RecordBroadcast(os.path.basename(__file__))
reader.start()
