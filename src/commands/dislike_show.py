import mysql.connector
from src.utils.find_show_id import find_show_id
from src.utils.find_and_delete_recordings import find_and_delete_recordings
from src.utils import timer
from src.utils.KodiResource import KodiResource


def dislike_show():
    connection = mysql.connector.connect(user='root', database='koditv')
    cursor = connection.cursor()

    kodi = KodiResource()
    item_dict = kodi.player_get_item()

    add_dislikes_record = ("INSERT INTO dislikes "
                           "(show_ID)"
                           "VALUES (%s)")

    title = item_dict['title']
    show_id = find_show_id(title, cursor)

    if show_id:
        try:
            cursor.execute(add_dislikes_record, (show_id,))
        except mysql.connector.errors.IntegrityError:
            pass
    connection.commit()

    find_and_delete_recordings(title)
    print(title)

    timer_ids = timer.find_timer_ids(title, kodi)
    if len(timer_ids) > 0:
        print("deleting : ", title)
        timer.delete_timers(timer_ids, kodi)
