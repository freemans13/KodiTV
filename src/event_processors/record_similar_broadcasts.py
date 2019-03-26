import os
from src.utils.series_info import series_info
from src.utils.TimerManager import TimerManager
from src.utils.Dislikes import Dislikes
from src.utils.EventLogReader import EventLogReader
from src.utils.KodiResource import KodiResource
from src.utils.DatabaseResource import DatabaseResource
from src.utils.TheTvDbResource import TheTvDbResource


class RecordSimilarBroadcasts(EventLogReader):
    """
    Take a look at what the user usually watches and
    find other shows for similar genres with the same channels in the kodi programme guide and
    score the results in an ordered list, make timers for these in this order
    """
    def __init__(self, offset_filename):
        super(RecordSimilarBroadcasts, self).__init__(offset_filename)
        self.db = DatabaseResource()
        self.kodi = KodiResource()
        self.tvdb = TheTvDbResource()

    def on_event(self, event_dict):
        """
        :param event_dict: Contains 3 elements; date, event, item
        :return: None
        """
        # needs a trigger event from log
        fav_channel = ("select c.channel, count(c.channel) "
                       "from shows s "
                       "inner join show_channel_map m on s.show_ID = m.show_ID "
                       "inner join channels c on m.channel_ID = c.channel_ID "
                       "where s.disliked = 0 "
                       "group by c.channel "
                       "order by 2 desc ")

        fav_genre = ("select g.genre, count(m.genre_id) "
                     "from genres g "
                     "inner join show_genre_map m on g.genre_id = m.genre_id "
                     "inner join shows s on s.show_ID = m.show_ID "
                     "where s.disliked = 0 "
                     "group by genre "
                     "order by 2 desc ")

        print('---\nScanning for similar broadcasts...')

        fav_channels = []
        self.db.cursor.execute(fav_channel)
        for (fav_channel, fav_channel_count) in self.db.cursor:
            fav_channels.append((fav_channel, fav_channel_count))
        print('Top channels', fav_channels)

        fav_genres = []
        self.db.cursor.execute(fav_genre)
        for (fav_genre, fav_genre_count) in self.db.cursor:
            fav_genres.append((fav_genre, fav_genre_count))
        print('Top genres', fav_genres)

        dislikes = Dislikes(self.db.cursor)

        # For each of the favourite channels find a valid Kodi PVR channel ID.
        # Store this in channel_ids
        channel_ids = []
        pvr_channels = self.kodi.pvr_get_channels()
        for pvr_channel in pvr_channels:
            for (fav_channel, fav_channel_count) in fav_channels:
                if pvr_channel['label'] == fav_channel:
                    channel_ids.append((pvr_channel, fav_channel_count))

        # Populate timer_dict with Kodi broadcasts matching a favourite channel and favourite genre
        # Make sure we also store in the timer_dict value, 'channel', 'channel_popularity' and 'genre_popularity'
        timer_dict = {}
        for (pvr_channel, fav_channel_count) in channel_ids:
            channel_id = pvr_channel['channelid']
            broadcasts = self.kodi.pvr_get_broadcasts(channel_id)

            if broadcasts:
                for broadcast in broadcasts:
                    if dislikes.is_disliked(broadcast['title']):
                        print('Skipping disliked show %s' % broadcast['title'])
                        continue
                    if not series_info(broadcast['plot'])['episode'] == 0:
                        genres = broadcast['genre']
                        genre_popularity = []
                        match = False
                        for (fav_genre, fav_genre_count) in fav_genres:
                            for genre in genres:
                                if fav_genre == genre:
                                    genre_popularity.append(fav_genre_count)
                                    match = True

                        if match:
                            broadcast['channel'] = pvr_channel['label']
                            broadcast['channel_popularity'] = fav_channel_count
                            broadcast['genre_popularity'] = genre_popularity
                            timer_dict[broadcast["label"]] = broadcast

        # add rating from tvdb to each value in timer_dict, default rating is 0.7
        for title in timer_dict.keys():
            series_rating = 0.7 # default rating, should there be no rating found on thetvdb.com
            series_dict = self.tvdb.search_series(title)
            if series_dict:
                series_id = series_dict[0]['id']
                series_info_dict = self.tvdb.series_info(series_id)
                if series_info_dict:
                    rating = series_info_dict['siteRating']
                    if rating > 0:
                        series_rating = rating / 10
            timer_dict[title]["rating"] = series_rating
            print("Rating for %s is %s/10" % (title, series_rating * 10))

        # Create a list of timer candidates. Create a score for each candidate
        candidates = []
        for broadcast in timer_dict.values():
            sum_genre_pop = 0
            for genre_pop in broadcast['genre_popularity']:
                sum_genre_pop += genre_pop
            avg_genre_popularity = sum_genre_pop / len(broadcast['genre_popularity'])
            score = (broadcast['channel_popularity'] + avg_genre_popularity) / broadcast['rating']
            broadcast = {
                "title": broadcast['label'],
                "genre": broadcast['genre'],
                "channel": broadcast['channel'],
                "broadcastid": broadcast['broadcastid'],
                "score": score
            }
            candidates.append(broadcast)

        # Sort candidates by score, reverse order
        candidates = sorted(candidates, key=lambda sugg_dict: sugg_dict['score'], reverse=True)

#        pprint(candidates)

        # Add timers for the top 10 candidates only
        final_list = candidates[:10]
        for broadcast in final_list:
            print('Found similar broadcast "%s" %s on %s' % (
                broadcast['title'], broadcast['genre'], broadcast['channel']))
            #TimerManager().add_timer(broadcast['title'], broadcast['broadcastid'])


reader = RecordSimilarBroadcasts(os.path.basename(__file__))
reader.start()

# Use this instead of reader.start() for a one-off run of the code for development/testing
# reader.on_event({})
