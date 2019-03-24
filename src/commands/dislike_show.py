import mysql.connector
from src.utils.find_and_delete_recordings import find_and_delete_recordings
from src.utils.TimerManager import TimerManager
from src.utils.KodiResource import KodiResource
import src.parameters as parameters


def dislike_show():
    connection = mysql.connector.connect(user=parameters.DB_USER, database=parameters.DB_NAME)
    cursor = connection.cursor()

    kodi = KodiResource()
    item_dict = kodi.player_get_item()

    update_shows_with_dislikes = ("UPDATE shows "
                                  "SET disliked = 1 "
                                  "WHERE title = %s")

    title = item_dict['title']

    cursor.execute(update_shows_with_dislikes, (title,))
    connection.commit()

    find_and_delete_recordings(title)
    print(title)

    timer = TimerManager()
    timer_ids = timer.find_timer_ids(title)
    if len(timer_ids) > 0:
        print("deleting : ", title)
        timer.delete_timers(timer_ids)
