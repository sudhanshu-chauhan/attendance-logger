import json
from tornado.websocket import WebSocketHandler

active_clients = []


class SocketOutputHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("websocket opened")
        if self not in active_clients:
            active_clients.append(self)

    def on_message(self, message):
        self.write_message(json.loads(message))
        print(message)

    def on_close(self):
        print "websocket closed!"
        if self in active_clients:
            active_clients.remove(self)
