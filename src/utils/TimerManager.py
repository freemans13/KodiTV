from src.utils.KodiResource import KodiResource


class TimerManager(KodiResource):
    """
    This is an extension from the KodiResource class, this class manages all timers
    can be called to;
    . delete timers
    . add timers
    . find the timer_ids (uid of a timer)
    """
    def find_timer_ids(self, title):
        """
        gives all timer_ids for the given title

        :param title: the title of the current show

        :return: list of timer_ids
        """
        timer_ids = []
        timers = self.pvr_get_timers()
        for timer in timers:
            timer_title = timer['label']
            if title == timer_title:
                timer_ids.append(timer['timerid'])
        return timer_ids

    def add_timer(self, title, broadcast_id):
        """
        makes a post request to create a timer for the show

        :param1 title:  current broadcasts title
        :param2 broadcast_id: currently broadcast uid

        :return: None
        """
        if len(self.find_timer_ids(title)) == 0:
            self.pvr_add_timer(broadcast_id)
            print('Timer added for "%s"' % title)
        else:
            print('Timer already exists for "%s"' % title)

    def delete_timers(self, timer_ids):
        """
        makes a post request to TVHeadend to delete the timer for the given show

        :param timer_ids: list of timers/recordings to be deleted

        :return: Kodi response
        """
        for timer_id in timer_ids:
            self.pvr_delete_timer(timer_id)
        print(len(timer_ids), "done")
