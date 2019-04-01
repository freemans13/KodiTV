import requests
from src.utils.JsonRpcResource import JsonRpcResource


class KodiResource(JsonRpcResource):
    """
    This class extends the JsonRpcResource base class.
    This lists all Kodi requests
    Any request we want to make to kodi is made through this class

    """

    def pvr_get_channel_details(self, channel_id, fields=['broadcastnow']):
        """
        Gives channel details for a broadcast

        :param channel_id: channel we want details on

        :return: ^
        """
        return self.get('PVR.GetChannelDetails',
                        {
                            'channelid': channel_id,
                            'properties': fields
                        },
                        "channeldetails")

    def pvr_get_channels(self):
        """
        gets list of all channels

        :return: ^
        """
        return self.get('PVR.GetChannels',
                        {
                            "channelgroupid": "alltv"
                        },
                        'channels')

    def pvr_get_broadcasts(self, channel_id):
        """
        gets list of all broadcasts

        :param channel_id: channel we want details on

        :return: ^
        """
        return self.get('PVR.GetBroadcasts',
                        {
                            "channelid": channel_id,
                            "properties": [
                                "title",
                                "plot",
                                "plotoutline",
                                "starttime",
                                "endtime",
                                "runtime",
                                "progress",
                                "progresspercentage",
                                "genre",
                                "episodename",
                                "episodenum",
                                "episodepart",
                                "firstaired",
                                "hastimer",
                                "isactive",
                                "parentalrating",
                                "wasactive",
                                "thumbnail",
                                "rating",
                                "originaltitle",
                                "cast",
                                "director",
                                "writer",
                                "year",
                                "imdbnumber",
                                "hastimerrule",
                                "hasrecording",
                                "recording",
                                "isseries"
                            ]
                        },
                        'broadcasts')

    def player_get_item(self, quiet=False):
        """
        details of current show

        :return: ^
        """
        return self.get("Player.GetItem",
                        {"playerid": 1, "properties": ["title",
                                                       "artist",
                                                       "albumartist",
                                                       "genre",
                                                       "year",
                                                       "rating",
                                                       "album",
                                                       "track",
                                                       "duration",
                                                       "comment",
                                                       "lyrics",
                                                       "musicbrainztrackid",
                                                       "musicbrainzartistid",
                                                       "musicbrainzalbumid",
                                                       "musicbrainzalbumartistid",
                                                       "playcount",
                                                       "fanart",
                                                       "director",
                                                       "trailer",
                                                       "tagline",
                                                       "plot",
                                                       "plotoutline",
                                                       "originaltitle",
                                                       "lastplayed",
                                                       "writer",
                                                       "studio",
                                                       "mpaa",
                                                       "cast",
                                                       "country",
                                                       "imdbnumber",
                                                       "premiered",
                                                       "productioncode",
                                                       "runtime",
                                                       "set",
                                                       "showlink",
                                                       "streamdetails",
                                                       "top250",
                                                       "votes",
                                                       "firstaired",
                                                       "season",
                                                       "episode",
                                                       "showtitle",
                                                       "thumbnail",
                                                       "file",
                                                       "resume",
                                                       "artistid",
                                                       "albumid",
                                                       "tvshowid",
                                                       "setid",
                                                       "watchedepisodes",
                                                       "disc",
                                                       "tag",
                                                       "art",
                                                       "genreid",
                                                       "displayartist",
                                                       "albumartistid",
                                                       "description",
                                                       "theme",
                                                       "mood",
                                                       "style",
                                                       "albumlabel",
                                                       "sorttitle",
                                                       "episodeguide",
                                                       "uniqueid",
                                                       "dateadded",
                                                       "channel",
                                                       "channeltype",
                                                       "hidden",
                                                       "locked",
                                                       "channelnumber",
                                                       "starttime",
                                                       "endtime",
                                                       "specialsortseason",
                                                       "specialsortepisode",
                                                       "compilation",
                                                       "releasetype",
                                                       "albumreleasetype",
                                                       "contributors",
                                                       "displaycomposer",
                                                       "displayconductor",
                                                       "displayorchestra",
                                                       "displaylyricist",
                                                       "userrating"]},
                        'item',
                        quiet=quiet)

    def pvr_get_recording_details_batch(self, recording_ids):
        """
        through a certain few recordings in reocrdings list (its own request) get
        (through another request) details of the recordings

        :param recording_ids: uid for a recording

        :return: recordings details for relevant recordings
        """
        recordings_same_name = []
        for record_id in recording_ids:
            recordings_same_name.append(
                '''{"jsonrpc":"2.0","id":1,"method":"PVR.GetRecordingDetails","params":{"recordingid":''' +
                str(record_id) + ''',"properties":
                    [
                    "title",
                    "plot",
                    "plotoutline",
                    "genre",
                    "playcount",
                    "resume",
                    "channel",
                    "starttime",
                    "endtime",
                    "runtime",
                    "lifetime",
                    "icon",
                    "art",
                    "streamurl",
                    "file",
                    "directory",
                    "radio",
                    "isdeleted",
                    "epgeventid",
                    "channeluid"
                    ]
                    }}''')

        if len(recordings_same_name) > 10:
            print('Items exceeds the maximum allowed length')
            str_request = ','.join(map(str, recordings_same_name[:10]))
        else:
            str_request = ','.join(map(str, recordings_same_name))

        if len(recordings_same_name) > 0:
            print(self.http_url + '''?request=[''' + str_request + "]")
            response = requests.get(self.http_url + '''?request=[''' + str_request + ']')

            temp = response.json()
            result = []
            for row in temp:
                result.append(row['result']['recordingdetails'])
            return result
        return []

    def pvr_get_recordings(self):
        """
        gets list of recordings

        :return:^
        """
        return self.get("PVR.GetRecordings", {}, 'recordings')

    def player_stop(self):
        """
        stops the Kodi player (show)

        :return: Kodi response
        """
        self.post("Player.Stop", {"playerid": 1})

    def player_open(self, rec_to_post):
        """
        opens kodi player, and watches ...

        :param rec_to_post: the uid of the recording to be watched

        :return: Kodi response
        """
        self.post("Player.Open", {"item": {"recordingid": rec_to_post}})
        print("Player opened successfully ")

    def input_select(self):
        """
        simulates pressing the "okay" button

        :return: Kodi response
        """
        print("resume")
        self.post("Input.Select", {})

    def pvr_add_timer(self, broadcast_id):
        """
        adds a time for the current broadcast

        :param broadcast_id: the uid of the current broadcast

        :return: Kodi response
        """
        self.post("PVR.AddTimer", {"broadcastid": broadcast_id, "timerrule": True})

    def pvr_get_timers(self):
        """
        gets a list of all timers

        :return: ^
        """
        return self.get("PVR.GetTimers", {"properties": []}, "timers")

    def pvr_delete_timer(self, timer_id):
        """
        deletes the timer with ... uid

        :param timer_id: uid for the timer

        :return: Kodi response
        """
        self.post("PVR.DeleteTimer", {"timerid": timer_id})
