import json
import mysql.connector
import time
import datetime
from pygtail import Pygtail
import os
txt_files = []
file_name = ""

while True:
    if len(txt_files) == 0:
        # see https://stackoverflow.com/questions/5640630/array-filter-in-python
        txt_files = [entry for entry in os.listdir("event_logs/") if entry.endswith('.txt')]
        txt_files.sort()
        if file_name != "":
            # we know the last file_name we processed - no point re-loading older files
            txt_files = [file for file in txt_files if file > file_name]
    if len(txt_files) > 0:
        # grab oldest file in the array (first element) and remove it from the array
        file_name = txt_files.pop(0)
    if file_name == "":
        time.sleep(1)
    else:
        # print(file_name)

        connection = mysql.connector.connect(user='root', database='koditv')
        cursor = connection.cursor()

        current_programme = ""
        for line in Pygtail("event_logs/" + file_name, offset_file="event_logs/" + file_name + "." + os.path.basename(__file__) + ".offset"):
            log_dict = json.loads(line)
            if 'error' not in log_dict['item']:
                add_shows_record = ("INSERT INTO shows "
                                      "(date, title, channel) "
                                      "VALUES (%s, %s, %s)")
                data = ()
                # print("loop")
                if log_dict['item']['result']['item']['title'] == current_programme:
                    print(log_dict['event']['method'])
                else:
                    show_id = 0
                    current_programme = log_dict['item']['result']['item']['title']
                    try:

                        data = (
                            datetime.datetime.strptime(log_dict['date'], "%Y-%m-%d %H:%M:%S"),
                            log_dict['item']['result']['item']['title'],
                            log_dict['item']['result']['item']['channel'])

                        print(data)
                        # Insert new shows record
                        cursor.execute(add_shows_record, data)
                        show_id = cursor.lastrowid

                    except mysql.connector.errors.IntegrityError as e:
                        print('SQLError:', e)
                    except KeyError as e:
                        print('Error: cant find key', e)

                    add_genre_record = ("INSERT INTO genres "
                                        "(genre)"
                                        "VALUES (%s)")

                    select_from_genre = ("SELECT genre_ID from genres "
                                         "WHERE genre = %s")

                    select_time_of_event = ("SELECT date, title, show_ID from shows "
                                            "WHERE event_type = %s or show_ID = %s")
                    #
                    # select_next_record = ("SELECT shows_ID from shows "
                    #                       "WHERE ")

                    add_map_record = ("INSERT INTO show_genre_map "
                                      "(genre_ID, show_ID) "
                                      "VALUES (%s, %s)")

                    # repeat for every genre of the programme
                    for genre in log_dict['item']['result']['item']['genre']:

                        genre_id = 0
                        try:
                            # Insert new genre record
                            cursor.execute(add_genre_record, (genre, ))
                            # lastrow returns last given auto increment value
                            genre_id = cursor.lastrowid

                        except mysql.connector.errors.IntegrityError as e:
                            # find id of the duplicate genre, where the genre is already listed go through all other genres.
                            # print('Error:', e)
                            cursor.execute(select_from_genre, (genre, ))
                            for (ID) in cursor:
                                # formatted as touple so cheated
                                genre_id = ID[0]

                        # we now have show_id and genre_id
                        print(show_id, genre_id)

                        try:
                            cursor.execute(add_map_record, (genre_id, show_id))
                        except mysql.connector.errors.IntegrityError as e:
                            pass

                       # if cursor.execute(select_time_of_event, ("Player.OnPlay",)):
                       #  current_programme = cursor.title
                       #
                       #  while cursor.title == current_programme:
                       #
                       #      if log_dict['event']['method'] == "Player.OnPlay" or "Player.OnResume":
                       #          time_start = date
                       #          if event_type == "player.OnResume"
                       #


            # Make sure data is committed to the database
            connection.commit()

        cursor.close()
        connection.close()

        time.sleep(5)
