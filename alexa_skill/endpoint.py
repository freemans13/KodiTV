from http.server import BaseHTTPRequestHandler, HTTPServer
from src.commands.play_recommendation import play_something
import json
from src.commands.dislike_show import dislike_show
import time
from src.commands.stop_show import stop_show
from src.commands.watched_recording import watched_recording
import src.parameters as parameters

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print('do_GET')
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = self.path
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    def do_POST(self):
        print('do_POST')

        # read request BODY
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print(post_body)
        body_dict = json.loads(post_body)
        if not"intent" in body_dict['request']:
            # send HTTP status code for success
            self.send_response(400) # bad request

            self.send_header('Content-type', "application/json;charset=UTF-8")
            self.end_headers()

            # # send JSON response
            # message = """{"version": "1.0",
            #                         "response": {"outputSpeech": {
            #                         "type": "PlainText",
            #                         "text": "will do, playing %s",
            #                         "playBehavior": "REPLACE_ENQUEUED"}}}""" % title
            # print(message)
            # self.wfile.write(bytes(message, "utf8"))
            return

        intent = body_dict['request']['intent']['name']
        print(intent)
        if intent == "play":
            # send HTTP status code for success
            self.send_response(200)

            self.send_header('Content-type', "application/json;charset=UTF-8")
            self.end_headers()

            title = play_something()

            # send JSON response
            message = """{"version": "1.0", 
                        "response": {"outputSpeech": {
                        "type": "PlainText",
                        "text": "will do, playing %s", 
                        "playBehavior": "REPLACE_ENQUEUED"}}}""" % title
            print(message)
            self.wfile.write(bytes(message, "utf8"))
            return

        if intent == "dislike":
            # send HTTP status code for success
            self.send_response(200)

            self.send_header('Content-type', "application/json;charset=UTF-8")
            self.end_headers()

            dislike_show()
            stop_show()
            # time.sleep(parameters.DELAY)
            title = play_something()

            # send JSON response
            message = """{"version": "1.0", 
                                    "response": {"outputSpeech": {
                                    "type": "PlainText",
                                    "text": "yeah i agree, playing %s" , 
                                    "playBehavior": "REPLACE_ENQUEUED"}}}""" % title
            print(message)
            self.wfile.write(bytes(message, "utf8"))
            return

        if intent == "stop":
            # send HTTP status code for success
            self.send_response(200)

            self.send_header('Content-type', "application/json;charset=UTF-8")
            self.end_headers()

            stop_show()

            # send JSON response
            message = """{"version": "1.0", 
                                    "response": {"outputSpeech": {
                                    "type": "PlainText",
                                    "text": "okay, orey-ve-waar" , 
                                    "playBehavior": "REPLACE_ENQUEUED"}}}"""
            print(message)
            self.wfile.write(bytes(message, "utf8"))
            return

        if intent == "watched":
            # send HTTP status code for success
            self.send_response(200)

            self.send_header('Content-type', "application/json;charset=UTF-8")
            self.end_headers()

            title = watched_recording()
            # stop_show()
            time.sleep(parameters.DELAY)
            # new_title = ''
            new_title = play_something()

            # send JSON response
            message = """{"version": "1.0", 
                                    "response": {"outputSpeech": {
                                    "type": "PlainText",
                                    "text": "okay, %s, gone, playing %s" , 
                                    "playBehavior": "REPLACE_ENQUEUED"}}}""" % (title, new_title)
            print(message)
            self.wfile.write(bytes(message, "utf8"))
            return


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ("", 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()
