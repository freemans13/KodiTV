from datetime import datetime
import os
from src.utils.EventLogReader import EventLogReader
from src.commands.play_recommendation import play_something
from src.utils.find_and_delete_recordings import find_and_delete_recordings

# this exists as Kodi's JSONRPC doesnt allow you to delete recordings, therefore we used TvHeadend's WebAPI
# documentation on TvHeadend's WebAPI  https://github.com/dave-p/TVH-API-docs/wiki/Dvr


class DeleteFinishedRecordings(EventLogReader):
    def on_event(self, event_dict):
        if event_dict['event']['method'] == "Player.OnStop" or event_dict['event']['method'] == "VideoLibrary.OnUpdate":
            if event_dict['item']['resume']['position'] == -1:

                if 'starttime' not in event_dict['item']:
                    print('starttime not found :(')
                else:
                    title = event_dict['item']['label']
                    start = event_dict['item']['starttime']
                    end = event_dict['item']['endtime']
                    print("---\nAttempting to delete recording", title, start, end)

                    os.environ['TZ'] = 'Europe/London'
                    end_real = datetime.strptime(end + " BST", "%Y-%m-%d %H:%M:%S %Z").timestamp()

                    find_and_delete_recordings(title, end_real=end_real)

                    play_something()


reader = DeleteFinishedRecordings(os.path.basename(__file__))
reader.start()
