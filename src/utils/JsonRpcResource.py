import src.parameters as parameters
import requests
import json
from pprint import pprint


class JsonRpcResource:
    """
    This is a bass class, to make JSON-RPC requests, and receive JSON-RPC responses.

    refer to  https://kodi.wiki/view/JSON-RPC_API/v9
    """
    def __init__(self):
        self.http_url = parameters.KODI_HTTP_URL
        self.web_socket_url = parameters.KODI_WEBSOCKET_URL

    def get(self, method, params, response_key='', quiet=False):
        """
        manages get requests

        :param1 method: JSON-RPC method. e.g. PVR.GetRecordings
        :param2 params: Specific to the method what data you want returned
        :param3 response_key: Rather than return entire response only return relevant information

        :return: Response_Key or None or Response
        """
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
            elif not quiet:
                print('--------------------')
                print('%s - error response:' % method)
                pprint(response)
                print('--------------------')
        return None

    def post(self, method, params):
        """
        manages post requests

        :param method: JSON-RPC method. e.g. Player.Open
        :param params: Specific to the method

        :return: None
        """
        requests.post(self.http_url,
                      json={"jsonrpc": "2.0",
                            "id": 1,
                            "method": method,
                            "params": params})
