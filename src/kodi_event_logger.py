#!/usr/bin/env python

# WS client example
import asyncio
import websockets
import time
import datetime
import json
from src.utils.KodiResource import KodiResource
import src.parameters as parameters


async def event_listener():
    """
    This makes a websocket connection to Kodi and listens to all events raised, for each event raised,
    a JSON object is formatted as string adn is stored as a line in a log file.
    The log file naming convention is yyyy-mm-dd.txt adn the new file is created sunday 00:00 of every week

    Our websocket connection was based of this example:
    https://pypi.org/project/websockets/

    :return: None
    """
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

            row = '{"date": "' + now.strftime("%Y-%m-%d %H:%M:%S") + '", "event": ' + event + ', "item": ' + json.dumps(
                event_data) + '}'

            # calculate name of the file, this row should be saved to,
            # sunday 00:00 of every week
            week_start = now - datetime.timedelta(days=now.isoweekday() % 7)
            file_name = week_start.strftime("%Y-%m-%d") + ".txt"
            print(file_name, row)

            if log is None or file_name != log.name:
                if log:
                    #  the currently open file is no the log we want to save to, so close it
                    log.close()
                # open the new file in 'append' mode
                log = open(parameters.EVENT_LOG_PATH + file_name, 'a')

            log.write(row + '\n')
            # flush contents of python file writing buffer to file,
            # makes sure what we've written is immediately inserted
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
