from http.server import BaseHTTPRequestHandler, HTTPServer
from src.commands.play_something import play_something
import json
from src.commands.dislike_show import dislike_show
import time
from src.commands.stop_show import stop_show
from src.commands.watched_recording import watched_recording
import src.parameters as parameters


class AlexaSkillEndPoint(BaseHTTPRequestHandler):
    """
    This is the alexa skill endpoint, all alexa intents are sent to this endpoint.
    This is the simplest implementation based on an example from;
    https://hashnode.com/post/building-a-simple-rest-api-in-python-using-no-outside-dependencies-cin8g3t6100ducw53wrb1qeu5
    """

    def send_alexa_response(self, text):
        """
        Send formatted alexa response

        :param text:
                Sentence for alexa to say in response
        :return:
                None
        """

        # send HTTP status code for success
        self.send_response(200)

        self.send_header('Content-type', "application/json;charset=UTF-8")
        self.end_headers()

        # send JSON response
        message = {
            "version": "1.0",
            "response": {"outputSpeech": {
                "type": "PlainText",
                "text": text,
                "playBehavior": "REPLACE_ENQUEUED"}
            }
        }
        print(message)
        self.wfile.write(bytes(json.dumps(message), "utf8"))
        return

    def do_POST(self):
        """
        receiving POST request from alexa skill

        managing intents

        :return:
                None
        """

        print('do_POST')

        # read request BODY
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print(post_body)
        body_dict = json.loads(post_body)
        if "intent" not in body_dict['request']:
            # send HTTP status code for success
            self.send_response(400)  # bad request

            self.send_header('Content-type', "application/json;charset=UTF-8")
            self.end_headers()
            return

        intent = body_dict['request']['intent']['name']
        print(intent)

        if intent == "play":
            title = play_something()

            self.send_alexa_response("will do, playing %s" % title)
            return

        if intent == "dislike":
            dislike_show()
            stop_show()
            # time.sleep(parameters.DELAY)
            title = play_something()

            self.send_alexa_response("yeah i agree, I don't like it either, playing %s" % title)
            return

        if intent == "stop":
            stop_show()

            self.send_alexa_response("okay, orey-ve-waar")
            return

        if intent == "watched":
            title = watched_recording()
            # stop_show()
            time.sleep(parameters.DELAY)
            # new_title = ''
            new_title = play_something()

            self.send_alexa_response("okay, %s, gone, playing %s" % (title, new_title))
            return


def run():
    """
    start endpoint

    :return:
            None
    """

    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ("", 8081)
    httpd = HTTPServer(server_address, AlexaSkillEndPoint)
    print('running server...')
    httpd.serve_forever()


run()
