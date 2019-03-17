import mysql.connector
from src.utils.series_info import series_info
from pprint import pprint
from src.utils.Dislikes import Dislikes
from src.utils.KodiResource import KodiResource


def processor(connection, cursor, log_dict):
    # needs a trigger event from log
    fav_channel = ("select channel, count(channel) "
                   "from shows group by channel order by 2 desc limit 5")

    fav_genre = ("select g.genre, count(m.genre_id) "
                 "from genres g inner join show_genre_map m on g.genre_id = m.genre_id "
                 "group by genre order by 2 desc limit 5")

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
                channel_ids.append(channel['channelid'])

    for channel_id in channel_ids:
        epg_dict = kodi.pvr_get_broadcasts(channel_id)

        if epg_dict:
            for broadcast in epg_dict:
                if dislikes.is_disliked(broadcast['title']):
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
                        timer_dict[broadcast["label"]] = broadcast['broadcastid']
    pprint(timer_dict)
    # for title in timer_dict.keys():
    #     add_timer(title, timer_dict[title], kodi)


connection = mysql.connector.connect(user='root', database='koditv')
cursor = connection.cursor()
processor(connection, cursor, None)
cursor.close()
connection.close()
