import requests
from src.utils.JsonRpcResource import JsonRpcResource


class KodiResource(JsonRpcResource):

    def pvr_get_channel_details(self, channel_id):
        return self.get('PVR.GetChannelDetails',
                        {
                            'channelid': channel_id,
                            'properties': ['broadcastnow']
                        },
                        "channeldetails")

    def pvr_get_channels(self):
        return self.get('PVR.GetChannels',
                        {
                            "channelgroupid": "alltv"
                        },
                        'channels')

    def pvr_get_broadcasts(self, channel_id):
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

    def player_get_item(self):
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
                        'item')

    def pvr_get_recording_details_batch(self, recording_ids):
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
        return self.get("PVR.GetRecordings", {}, 'recordings')

    def player_stop(self):
        self.post("Player.Stop", {"playerid": 1})

    def player_open(self, rec_to_post):
        self.post("Player.Open", {"item": {"recordingid": rec_to_post}})
        print("Player opened successfully ")

    def input_select(self):
        print("resume")
        self.post("Input.Select", {})

    def pvr_add_timer(self, broadcast_id):
        self.post("PVR.AddTimer", {"broadcastid": broadcast_id, "timerrule": True})

    def pvr_get_timers(self):
        return self.get("PVR.GetTimers", {"properties": []}, "timers")

    def pvr_delete_timer(self, timer_id):
        self.post("PVR.DeleteTimer", {"timerid": timer_id})
