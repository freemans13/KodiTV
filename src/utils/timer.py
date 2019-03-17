from src.utils.KodiResource import KodiResource


def find_timer_ids(title, kodi: KodiResource):
    timer_ids = []
    timers = get_timers(kodi)
    for timer in timers:
        timer_title = timer['label']
        if title == timer_title:
            timer_ids.append(timer['timerid'])
    return timer_ids


def add_timer(title, broadcast_id, kodi: KodiResource):
    if len(find_timer_ids(title, kodi)) == 0:
        print(broadcast_id, "timer added", title)
        kodi.pvr_add_timer(broadcast_id)


def get_timers(kodi: KodiResource):
    timers = kodi.pvr_get_timers()
    return timers


def delete_timers(timer_ids, kodi: KodiResource):
    for timer_id in timer_ids:
        kodi.pvr_delete_timer(timer_id)

    print(len(timer_ids), "done")
