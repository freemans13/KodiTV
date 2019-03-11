from http.server import BaseHTTPRequestHandler, HTTPServer
from play_recommendation import play_something


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
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

    # POST
    def do_POST(self):
        print('do_POST')

        # read request BODY
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print(post_body)

        # send HTTP status code for success
        self.send_response(200)

        self.send_header('Content-type', "application/json;charset=UTF-8")
        self.end_headers()

        # send JSON response
        message = """{"version": "1.0", 
                    "response": {"outputSpeech": {
                    "type": "PlainText",
                    "text": "will do, ter dar", 
                    "playBehavior": "REPLACE_ENQUEUED"}}}"""
        print(message)
        self.wfile.write(bytes(message, "utf8"))
        play_something()
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