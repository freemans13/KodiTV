from src.utils.KodiResource import KodiResource


def stop_show():
    kodi = KodiResource()
    kodi.player_stop()
