import src.parameters as parameters
import requests
from pprint import pprint


class KodiResource:
    def __init__(self):
        self.http_url = parameters.KODI_HTTP_URL
        self.web_socket_url = parameters.KODI_WEBSOCKET_URL

    def pvr_get_channel_details(self, channel_id):
        response = requests.get(
            self.http_url + '''?request=
            {"jsonrpc":"2.0","id":1,"method":"PVR.GetChannelDetails","params":{"channelid":'''
            + str(channel_id) + ''',"properties": ["broadcastnow"]}}''')

        if response.status_code == 200:
            return response.json()["result"]["channeldetails"]
        return None

    def pvr_get_channels(self):
        response = requests.get(self.http_url + '''?request={"jsonrpc":"2.0","id":1,"method":"PVR.GetChannels",
                                                      "params":{
                                                          "channelgroupid":"alltv"
                                                       }}''')
        return response.json()['result']['channels']

    def pvr_get_broadcasts(self, channel_id):
        response = requests.get(self.http_url + '''?request=
              {"jsonrpc":"2.0","id":1,"method":"PVR.GetBroadcasts","params":{
               "channelid":''' + str(channel_id) + ''',"properties":["title",
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
         }}''')

        if response.status_code == 200:
            result = response.json()
            return result["result"]["broadcasts"]
        return None

    def player_get_item(self):
        response = requests.get(
            self.http_url + '''?request={"jsonrpc":"2.0","id":1,"method":"Player.GetItem", "params":{"playerid":1,"properties":["title",
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
             "userrating"]}}''')

        if response.status_code == 200:
            result = response.json()
            if 'result' in result:
                return result['result']['item']
            else:
                print('player.getitem - error response', result)
        return None

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
        response = requests.get(self.http_url + '''?request={"jsonrpc":"2.0","id":1,"method":"PVR.GetRecordings"}''')
        record_dict = response.json()['result']['recordings']
        pprint(record_dict)
        return record_dict

    def player_stop(self):
        requests.post(self.http_url,
                      json={"jsonrpc": "2.0", "id": 1,
                            "method": "Player.Stop",
                            "params": {"playerid": 1}})

    def player_open(self, rec_to_post):
        requests.post(self.http_url,
                      json={"jsonrpc": "2.0", "id": 1,
                            "method": "Player.Open",
                            "params": {"item": {"recordingid": rec_to_post}}})
        print("good job ")

    def input_select(self):
        print("resume")
        requests.post(self.http_url,
                      json={"jsonrpc": "2.0", "id": 1, "method": "Input.Select"})

    def pvr_add_timer(self, broadcast_id):
        r = requests.post(self.http_url,
                          json={"jsonrpc": "2.0", "id": 1,
                                "method": "PVR.AddTimer",
                                "params": {"broadcastid": broadcast_id, "timerrule": True}})
        print(r.status_code, r.reason)

    def pvr_get_timers(self):
        r = requests.get(self.http_url + '''?request=
                           {"jsonrpc":"2.0","id":1,"method":"PVR.GetTimers","params":{"properties":[]}}''')
        timers = r.json()
        return timers['result']['timers']

    def pvr_delete_timer(self, timer_id):
        requests.post(self.http_url,
                      json={"jsonrpc": "2.0", "id": 1, "method": "PVR.DeleteTimer", "params":
                          {"timerid": timer_id}})
