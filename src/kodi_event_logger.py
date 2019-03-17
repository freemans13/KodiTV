#!/usr/bin/env python

# WS client example
from src import parameters
import asyncio
import websockets
import time
import datetime
import json
from src.utils.KodiResource import KodiResource


async def event_listener():
    async with websockets.connect(parameters.KODI_WEBSOCKET_URL, ping_interval=None) as websocket:
        print('Kodi connected')
        await websocket.send(
            '{"jsonrpc":"2.0","method":"JSONRPC.NotifyAll","params": { "sender": "tom", "message": "x" }}')
        log = None
        kodi = KodiResource()

        async for message in websocket:
            event = await websocket.recv()
            now = datetime.datetime.now()

            event_data = kodi.player_get_item()

            # row = now.strftime("%Y-%m-%d %H:%M:%S") + event + event_data
            row = '{"date": "' + now.strftime("%Y-%m-%d %H:%M:%S") + '", "event": ' + event + ', "item": ' + json.dumps(
                event_data) + '}'

            week_start = now - datetime.timedelta(days=now.isoweekday() % 7)
            file_name = week_start.strftime("%Y-%m-%d") + ".txt"
            print(file_name, row)

            if log is None or file_name != log.name:
                if log:
                    log.close()
                log = open("../event_logs/" + file_name, 'a')

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
