from src.utils.KodiResource import KodiResource


def stop_show():
    """
    Tells Kodi to stop playing
    :return: None
    """
    kodi = KodiResource()
    kodi.player_stop()
