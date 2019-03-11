import requests
import json
import mysql.connector
import parameters


def is_series(broadcast_dict):
    # if broadcast_dict['is_series'] is True or broadcast_dict['episodenum'] != 0:
    return True
    # elif broadcast_dict['plot']:


# def episode_status():


def processor(connection, cursor, log_dict):
    # needs a trigger event from log
    fav_channel = ("select channel_number, count(channel_number) from shows group by channel_number order by 2 desc limit 5")

    fav_genre = ("select g.genre, count(m.genre_id) "
                 "from genres g inner join show_genre_map m on g.genre_id = m.genre_id "
                 "group by genre order by 2 desc limit 5")

    channels = []
    cursor.execute(fav_channel)
    for (channel_number, channel_count) in cursor:
        channels.append(channel_number)

    print('Top channels', channels)

    genre_rating = []
    cursor.execute(fav_genre)
    for (genre, genre_count) in cursor:
        genre_rating.append(genre)
    print('Top genres', genre_rating)

    for channelid in channels:
        response = requests.get(parameters.KODI_HTTP_URL + '''?request=
             {"jsonrpc":"2.0","id":1,"method":"PVR.GetBroadcasts","params":{
              "channelid":''' + str(channelid) + ''',"properties":["title",
              "plot",
              "plotoutline",
              "starttime",
              "endtime",
              "runtime",
              "progress",
              "progresspercentage",
              "genre",
              "episodename",
              "episodenum",
              "episodepart",
              "firstaired",
              "hastimer",
              "isactive",
              "parentalrating",
              "wasactive",
              "thumbnail",
              "rating",
              "originaltitle",
              "cast",
              "director",
              "writer",
              "year",
              "imdbnumber",
              "hastimerrule",
              "hasrecording",
              "recording",
              "isseries"
            ]
        }}''')

        if response.status_code == 200:
            broadcast_details = response.text
            epg_dict = json.loads(broadcast_details)

        if 'result' in epg_dict:
            for broadcast in epg_dict['result']['broadcasts']:
                if is_series(broadcast):
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
                        print(broadcast['label'], broadcast['starttime'], broadcast['genre'])


connection = mysql.connector.connect(user='root', database='koditv')
cursor = connection.cursor()
processor(connection, cursor, None)
cursor.close()
connection.close()