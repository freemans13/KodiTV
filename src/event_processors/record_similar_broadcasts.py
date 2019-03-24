import mysql.connector
from src.utils.series_info import series_info
from src.utils.TimerManager import TimerManager
from src.utils.Dislikes import Dislikes
from src.utils.EventLogReader import EventLogReader
from src.utils.KodiResource import KodiResource
from src.utils.DatabaseResource import DatabaseResource


def processor(connection, cursor, event_dict):
    # needs a trigger event from log
    fav_channel = ("select c.channel, count(c.channel) "
                   "from shows s "
                   "inner join show_channel_map m on s.show_ID = m.show_ID "
                   "inner join channels c on m.channel_ID = c.channel_ID "
                   "where s.disliked = 0 "
                   "group by c.channel "
                   "order by 2 desc "
                   "limit 5")

    fav_genre = ("select g.genre, count(m.genre_id) "
                 "from genres g "
                 "inner join show_genre_map m on g.genre_id = m.genre_id "
                 "inner join shows s on s.show_ID = m.show_ID "                 
                 "where s.disliked = 0 "
                 "group by genre "
                 "order by 2 desc "
                 "limit 5")

    print('---\nScanning for similar broadcasts...')

    fav_channel_names = []
    cursor.execute(fav_channel)
    for (channel, channel_count) in cursor:
        fav_channel_names.append(channel)

    print('Top channels', fav_channel_names)

    genre_rating = []
    cursor.execute(fav_genre)
    for (genre, genre_count) in cursor:
        genre_rating.append(genre)
    print('Top genres', genre_rating)

    kodi = KodiResource()
    dislikes = Dislikes(cursor)

    channel_ids = []
    timer_dict = {}
    channels = kodi.pvr_get_channels()
    for channel in channels:
        for fav_channel in fav_channel_names:
            if channel['label'] == fav_channel:
                channel_ids.append(channel)

    for channel in channel_ids:
        channel_id = channel['channelid']
        epg_dict = kodi.pvr_get_broadcasts(channel_id)

        if epg_dict:
            for broadcast in epg_dict:
                if dislikes.is_disliked(broadcast['title']):
                    print('Skipping disliked show %s' % broadcast['title'])
                    continue
                if not series_info(broadcast['plot'])['episode'] == 0:
                    genres = broadcast['genre']
                    match = False
                    for genre in genre_rating:
                        for broadcast_genre in genres:
                            if genre == broadcast_genre:
                                match = True
                                break
                            if match:
                                break
                    if match:
                        # print(broadcast['label'], broadcast['starttime'],
                        # broadcast['genre'], broadcast['broadcastid'])
                        broadcast['channel'] = channel['label']
                        timer_dict[broadcast["label"]] = broadcast
    # pprint(timer_dict)
    for title in timer_dict.keys():
        print('Found similar broadcast "%s" %s on %s' % (title, timer_dict[title]['genre'], timer_dict[title]['channel']))
        TimerManager().add_timer(title, timer_dict[title]['broadcastid'])


class RecordSimilarBroadcasts(EventLogReader):
    def __init__(self, offset_filename):
        super(RecordSimilarBroadcasts, self).__init__(offset_filename)
        self.db = DatabaseResource()

    def on_event(self, event_dict):
        processor(self.db.connection, self.db.cursor, event_dict)


#reader = RecordSimilarBroadcasts(os.path.basename(__file__))
#reader.start()

con = mysql.connector.connect(user='root', database='koditv')
cur = con.cursor()
processor(con, cur, None)
cur.close()
con.close()
