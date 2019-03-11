#!/usr/bin/env python

# WS client example
import parameters
import asyncio
import websockets
import time
import datetime
import requests


async def event_listener():
    async with websockets.connect(parameters.KODI_WEBSOCKET_URL, ping_interval=None) as websocket:
        print('Kodi connected')
        await websocket.send('{"jsonrpc":"2.0","method":"JSONRPC.NotifyAll","params": { "sender": "tom", "message": "x" }}')
        log = None

        async for message in websocket:
            event = await websocket.recv()
            now = datetime.datetime.now()

            response = requests.get(
                parameters.KODI_HTTP_URL + '''?request={"jsonrpc":"2.0","id":1,"method":"Player.GetItem", "params":{"playerid":1,"properties":["title",
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
            event_data = '{}'
            if response.status_code == 200:
                event_data = response.text

            # row = now.strftime("%Y-%m-%d %H:%M:%S") + event + event_data
            row = '{"date": "' + now.strftime("%Y-%m-%d %H:%M:%S") + '", "event": ' + event + ', "item": ' + event_data + '}'

            week_start = now - datetime.timedelta(days=now.isoweekday() % 7)
            file_name = week_start.strftime("%Y-%m-%d") + ".txt"
            print(file_name, row)

            if log is None or file_name != log.name:
                if log:
                    log.close()
                log = open("event_logs/" + file_name, 'a')

            log.write(row + '\n')
            log.flush()



while True:
    try:
        asyncio.get_event_loop().run_until_complete(event_listener())
    except ConnectionRefusedError:
        print('Kodi not running. retry in 5 seconds')
        time.sleep(5)
    except websockets.exceptions.ConnectionClosed:
        print('Kodi connection closed. Retry in 10 seconds')
        time.sleep(10)
    # except requests.exceptions.ConnectionError as e:
    #     print('Kodi connection aborted. Retry in 10 seconds', e)
    #     time.sleep(10)
