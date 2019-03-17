import mysql.connector
import datetime
from src.utils.read_logs import read_logs
from src.utils.series_info import series_info
import os
from src.utils.find_show_id import find_show_id


def processor(connection, cursor, log_dict):
    if 'error' in log_dict['item']:
        return

    item = log_dict['item']
    if 'channel' not in item:
        print('missing channel?', item)
        return

    add_shows_record = ("INSERT INTO shows "
                        "(date, title, channel, channel_number) "
                        "VALUES (%s, %s, %s, %s)")

    try:

        data = (
            datetime.datetime.strptime(log_dict['date'], "%Y-%m-%d %H:%M:%S"),
            item['title'],
            item['channel'],
            item['id'])

        print(data)
        # Insert new shows record
        cursor.execute(add_shows_record, data)
        # Get show_id of newly inserted row
        show_id = cursor.lastrowid

    except mysql.connector.errors.IntegrityError as e:
        show_id = find_show_id(item['title'], cursor)

    add_genre_record = ("INSERT INTO genres "
                        "(genre)"
                        "VALUES (%s)")

    select_from_genre = ("SELECT genre_ID from genres "
                         "WHERE genre = %s")

    add_map_record = ("INSERT INTO show_genre_map "
                      "(genre_ID, show_ID) "
                      "VALUES (%s, %s)")

    add_episode_record = ("INSERT INTO episodes "
                          "(show_ID, season, episode, plot) "
                          "VALUES (%s, %s, %s, %s)")

    # repeat for every genre of the programme
    for genre in item['genre']:

        genre_id = 0
        try:
            # Insert new genre record
            cursor.execute(add_genre_record, (genre,))
            # lastrow returns last given auto increment value
            genre_id = cursor.lastrowid

        except mysql.connector.errors.IntegrityError as e:
            # find id of the duplicate genre, where the genre is already listed go through all other genres.
            # print('Error:', e)
            cursor.execute(select_from_genre, (genre,))
            for (ID,) in cursor:
                genre_id = ID

        # we now have show_id and genre_id
        print(show_id, genre_id)

        try:
            cursor.execute(add_map_record, (genre_id, show_id))
        except mysql.connector.errors.IntegrityError:
            pass

        plot = item['plot']
        result = series_info(plot)
        season = result['season']
        episode = result['episode']
        try:
            cursor.execute(add_episode_record, (show_id, season, episode, plot))
        except mysql.connector.errors.IntegrityError:
            pass

    # Make sure data is committed to the database
    connection.commit()


read_logs(processor, os.path.basename(__file__))
