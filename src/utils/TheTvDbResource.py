import src.parameters as parameters
import requests
from pprint import pprint


class TheTvDbResource:
    """
    This lets me access the tvdb api,
    automatically logins using my apikey adn returns the returned token
    to make any get or post requests

    https://api.thetvdb.com/swagger#!/Search/get_search_series
    """
    def __init__(self):
        self.token = None
        self.login()

    def get(self, path, params, response_key=''):
        """
        makes a rest http call to tvdb API passing in JWT token supplied by login

        :param path: the query path
        :param params: optional paramters associated with the request
        :param response_key: optional response key to filter json response

        :return: None if error or JSON data
        """
        response = requests.get(parameters.TVDB_HTML_URL + path, params=params,
                                headers={'Authorization': 'Bearer ' + self.token})
        if response.status_code == 200:
            response = response.json()
            if 'data' in response:
                response = response['data']
                if response_key in response:
                    return response[response_key]
                else:
                    return response
            else:
                print('--------------------')
                pprint(response)
                print('--------------------')
        return None

    def post(self, path, params):
        """
        makes a post request to the tvdb API server

        :param path: the query path
        :param params: optional paramters associated with the request

        :return: None if error or JSON data
        """
        response = requests.post(parameters.TVDB_HTML_URL + path, json=params)
        if response.status_code == 200:
            return response.json()
        else:
            print('--------------------')
            pprint(response)
            print('--------------------')
            return None

    def login(self):
        """
        using my api key from tvdb as authorisation.
        to obtain the token

        :return:
        """
        response = self.post('login', {'apikey': parameters.APIKEY})
        if 'token' in response:
            self.token = response['token']
            return True
        else:
            print('Login failed. No token available')
            return False

    def search_series(self, name):
        response = self.get('search/series', {'name': name})
        return response

    def series_info(self, series_id):
        response = self.get('series/' + str(series_id), None)
        return response
