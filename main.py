import json
import os

from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
from tornado.web import Application
from tornado.web import StaticFileHandler

from components import db_handler


active_clients = []


def send_data_to_clients(message):
    print "active cleints {}".format(len(active_clients))
    for client in active_clients:
        try:
            client.write_message(message)
        except Exception as err:
            print "websocket err: {}".format(err.message)
            active_clients.remove(client)


class SocketOutputHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print "websocket opened"
        if self not in active_clients:
            active_clients.append(self)

    def on_message(self, message):
        self.write_message(json.loads(message))
        print message

    def on_close(self):
        print "websocket closed!"
        if self in active_clients:
            active_clients.remove(self)


class DashboardHandler(RequestHandler):
    def get(self):
        self.render("./template/index.html")


class EmployeeInputHandler(RequestHandler):
    def post(self, *args, **kwargs):
        data = self.request.body
        response_data = db_handler.save_employee_data(data)
        send_data_to_clients(response_data)


class MainApplication(Application):
    def __init__(self):
        handlers = [
            (r"/get_attendance_data/", SocketOutputHandler),
            (r"/save_attendance_data/", EmployeeInputHandler),
            (r"/dashboard/", DashboardHandler),
            (r"/static/(.*)",
             StaticFileHandler,
             {'path': os.path.join(os.curdir, "template", "assets")})
        ]
        Application.__init__(self, handlers)


def main():
    app_instance = MainApplication()
    print("[*] starting socket app at 8001")
    app_instance.listen(8001)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()

