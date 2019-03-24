import src.parameters as parameters
import requests
import json
from pprint import pprint


class JsonRpcResource:
    def __init__(self):
        self.http_url = parameters.KODI_HTTP_URL
        self.web_socket_url = parameters.KODI_WEBSOCKET_URL

    def get(self, method, params, response_key=''):
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        response = requests.get(self.http_url + '?request=' + json.dumps(request))

        if response.status_code == 200:
            response = response.json()
            if 'result' in response:
                response = response['result']
                if response_key in response:
                    return response[response_key]
                else:
                    return response
            else:
                print('--------------------')
                print('%s - error response:' % method)
                pprint(response)
                print('--------------------')
        return None

    def post(self, method, params):
        requests.post(self.http_url,
                      json={"jsonrpc": "2.0",
                            "id": 1,
                            "method": method,
                            "params": params})
