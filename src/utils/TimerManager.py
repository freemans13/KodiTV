from src.utils.KodiResource import KodiResource


class TimerManager(KodiResource):
    def find_timer_ids(self, title):
        timer_ids = []
        timers = self.pvr_get_timers()
        for timer in timers:
            timer_title = timer['label']
            if title == timer_title:
                timer_ids.append(timer['timerid'])
        return timer_ids

    def add_timer(self, title, broadcast_id):
        if len(self.find_timer_ids(title)) == 0:
            self.pvr_add_timer(broadcast_id)
            print('Timer added for "%s"' % title)
        else:
            print('Timer already exists for "%s"' % title)

    def delete_timers(self, timer_ids):
        for timer_id in timer_ids:
            self.pvr_delete_timer(timer_id)
        print(len(timer_ids), "done")
