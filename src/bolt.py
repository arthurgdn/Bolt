from http.server import HTTPServer, BaseHTTPRequestHandler

class Server:

    def __init__(self,port):
        self.port = port
    def serve(self):
        httpd = HTTPServer(('localhost', self.port), BaseHTTPRequestHandler)
        httpd.serve_forever()

    


