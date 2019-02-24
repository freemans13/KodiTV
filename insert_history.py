import json
import mysql.connector
import time
import datetime

# while True:
week_start = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().isoweekday() % 7)
with open("event_logs/" + week_start.strftime("%Y-%m-%d") + ".txt") as log_file:
    line = log_file.readline()
    connection = mysql.connector.connect(user='root', database='koditv')
    cursor = connection.cursor()

    while line:
        log_dict = json.loads(line)

        if 'error' not in log_dict['item']:
            add_history_record = ("INSERT INTO history "
                                  "(date, title, channel, channel_number, event_type) "
                                  "VALUES (%s, %s, %s, %s, %s)")

            data = ()

            try:

                data = (
                    datetime.datetime.strptime(log_dict['date'], "%Y-%m-%d %H:%M:%S"),
                    log_dict['item']['result']['item']['title'],
                    log_dict['item']['result']['item']['channel'],
                    log_dict['item']['result']['item']['channelnumber'],
                    log_dict['event']['method']
                )

                print(data)
                # Insert new history record
                cursor.execute(add_history_record, data)
                history_id = cursor.lastrowid

            except KeyError as e:
                print('Error: cant find key', e)

            add_genre_record = ("INSERT INTO genres "
                                "(genre)"
                                "VALUES (%s)")

            select_from_genre = ("SELECT genre_ID from genres "
                                 "WHERE genre = %s")

            add_map_record = ("INSERT INTO history_genre_map "
                              "(genre_ID, history_ID) "
                              "VALUES (%s, %s)")

            for genre in log_dict['item']['result']['item']['genre']:

                genre_id = 0
                try:
                    # Insert new genre record
                    cursor.execute(add_genre_record, (genre, ))
                    genre_id = cursor.lastrowid

                except mysql.connector.errors.IntegrityError as e:
                    # find id of the duplicate genre
                    # print('Error:', e)
                    cursor.execute(select_from_genre, (genre, ))
                    for (ID) in cursor:
                        genre_id = ID[0]

                # we now have history_id and genre_id
                print(history_id, genre_id)

                cursor.execute(add_map_record, (genre_id, history_id))

        # Make sure data is committed to the database
        connection.commit()

        line = log_file.readline()

    cursor.close()
    connection.close()

        # time.sleep(30)

