import mysql.connector
import datetime
from src.utils.series_info import series_info
import os
from src.utils.find_show_id import find_show_id
from src.utils.EventLogReader import EventLogReader
from src.utils.DatabaseResource import DatabaseResource


class StoreShowDetails(EventLogReader):
    def __init__(self, offset_filename):
        super(StoreShowDetails, self).__init__(offset_filename)
        self.db = DatabaseResource()

    def on_event(self, event_dict):
        if event_dict['item'] is None:
            return
        if 'error' in event_dict['item']:
            return

        item = event_dict['item']
        if 'channel' not in item:
            print('missing channel?', item)
            return

        insert_show_sql = ("INSERT INTO shows "
                           "(date, title) "
                           "VALUES (%s, %s)")

        insert_genre_sql = ("INSERT INTO genres "
                            "(genre)"
                            "VALUES (%s)")

        find_genre_id_sql = ("SELECT genre_ID "
                             "FROM genres "
                             "WHERE genre = %s")

        insert_map_sql = ("INSERT INTO show_genre_map "
                          "(genre_ID, show_ID) "
                          "VALUES (%s, %s)")

        insert_episode_sql = ("INSERT INTO episodes "
                              "(show_ID, season, episode, plot) "
                              "VALUES (%s, %s, %s, %s)")

        insert_channel_sql = ("INSERT INTO channels "
                              "(channel)"
                              "VALUES (%s)")

        find_channel_id_sql = ("SELECT channel_ID "
                               "FROM channels "
                               "WHERE channel = %s")

        insert_show_channel_map_sql = ("INSERT INTO show_channel_map "
                                       "(channel_ID, show_ID) "
                                       "VALUES (%s, %s)")

        print('---\nStoring info on "%s"' % item['title'])

        try:

            data = (
                datetime.datetime.strptime(event_dict['date'], "%Y-%m-%d %H:%M:%S"),
                item['title'])

            # Insert new shows record
            self.db.cursor.execute(insert_show_sql, data)
            # Get show_id of newly inserted row
            show_id = self.db.cursor.lastrowid
            print('Inserted new Shows record show_ID:%s %s' % (show_id, data))

        except mysql.connector.errors.IntegrityError:
            show_id = find_show_id(item['title'], self.db.cursor)
            print('Show "%s" already exists; show_ID %s' % (item['title'], show_id))

        # repeat for every genre of the programme
        for genre in item['genre']:

            genre_id = 0
            try:
                # Insert new genre record
                self.db.cursor.execute(insert_genre_sql, (genre,))
                # lastrowid returns last given auto increment value
                genre_id = self.db.cursor.lastrowid
                print('Inserted new Genres record genre_ID:%s %s' % (genre_id, genre))

            except mysql.connector.errors.IntegrityError:
                # find id of the duplicate genre
                self.db.cursor.execute(find_genre_id_sql, (genre,))
                for (ID,) in self.db.cursor:
                    genre_id = ID
                    print('Genre "%s" already exists; genre_ID %s' % (genre, genre_id))

            try:
                self.db.cursor.execute(insert_map_sql, (genre_id, show_id))
                print('Inserted new Shows_Genres_Map record genre_ID:%s show_ID:%s' % (genre_id, show_id))
            except mysql.connector.errors.IntegrityError:
                pass

            plot = item['plot']
            result = series_info(plot)
            season = result['season']
            episode = result['episode']
            try:
                self.db.cursor.execute(insert_episode_sql, (show_id, season, episode, plot))
                print('Inserted new Episodes record show_ID:%s S%sE%s %s' % (show_id, season, episode, plot))
            except mysql.connector.errors.IntegrityError:
                pass

        channel_id = 0
        channel = item['channel']
        try:
            # Insert new channel record
            self.db.cursor.execute(insert_channel_sql, (channel,))
            # lastrowid returns last given auto increment value
            channel_id = self.db.cursor.lastrowid
            print('Inserted new channels record channel_ID:%s %s' % (channel_id, channel))

        except mysql.connector.errors.IntegrityError as e:
            # find id of the duplicate channel
            self.db.cursor.execute(find_channel_id_sql, (channel,))
            for (ID,) in self.db.cursor:
                channel_id = ID
                print('Channel "%s" already exists; channel_ID %s' % (channel, channel_id))

        try:
            self.db.cursor.execute(insert_show_channel_map_sql, (channel_id, show_id))
            print('Inserted new show_channel_map record channel_ID:%s show_ID:%s' % (channel_id, show_id))
        except mysql.connector.errors.IntegrityError:
            pass

        # Make sure data is committed to the database
        self.db.connection.commit()


reader = StoreShowDetails(os.path.basename(__file__))
reader.start()
