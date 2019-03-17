from datetime import datetime
import os
from src.utils.read_logs import read_logs
from src.commands.play_recommendation import play_something
from src.utils.find_and_delete_recordings import find_and_delete_recordings

# this exists as Kodi's JSONRPC doesnt allow you to delete recordings, therefore we used TvHeadend's WebAPI
# documentation on TvHeadend's WebAPI  https://github.com/dave-p/TVH-API-docs/wiki/Dvr


def processor(connection, cursor, log_dict):
    if log_dict['event']['method'] == "Player.OnStop" or log_dict['event']['method'] == "VideoLibrary.OnUpdate":
        if log_dict['item']['resume']['position'] == -1:

            if 'starttime' not in log_dict['item']:
                print('starttime not found :(')
            else:
                title = log_dict['item']['label']
                start = log_dict['item']['starttime']
                end = log_dict['item']['endtime']
                print("deleted recording", title, start, end)

                os.environ['TZ'] = 'Europe/London'
                end_real = datetime.strptime(end + " BST", "%Y-%m-%d %H:%M:%S %Z").timestamp()

                find_and_delete_recordings(title, end_real=end_real)

                play_something()


read_logs(processor, os.path.basename(__file__))
