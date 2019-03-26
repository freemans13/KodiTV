from src.utils.TvHeadEndResource import TvHeadEndResource
from src.utils.KodiResource import KodiResource


def watched_recording():
    """
    When a recording that is being played has already been seen by the user, this method will delete the recording.
    Steps taken:
    1) Ask Kodi what is being played
    2) Find and delete recording using TVHeadend

    :return: None
    """
    kodi = KodiResource()
    tv = TvHeadEndResource()
    item_dict = kodi.player_get_item()

    title = item_dict['title']
    plot = item_dict['plot']

    if title == "":
        print("Current Kodi player doesn't have a title")
    else:
        tv.find_and_delete_recordings(title, plot=plot)

        print(title, plot)
    return title
