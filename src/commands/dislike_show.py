import mysql.connector
from src.utils.TvHeadEndResource import TvHeadEndResource
from src.utils.TimerManager import TimerManager
from src.utils.KodiResource import KodiResource
import src.parameters as parameters


def dislike_show():
    """
    Marks a shows as 'disliked'. This method takes several steps:
    1) asks Kodi what is being watched
    2) searches the Shows table for the same show
    3) updates the Show record with disliked = 1
    4) delete all recordings of the show
    5) delete any timers associated with the show

    :return:
            None
    """
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

    tv = TvHeadEndResource()
    tv.find_and_delete_recordings(title)
    print(title)

    timer = TimerManager()
    timer_ids = timer.find_timer_ids(title)
    if len(timer_ids) > 0:
        print("deleting : ", title)
        timer.delete_timers(timer_ids)
