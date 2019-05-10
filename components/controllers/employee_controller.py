from tornado.web import RequestHandler


class EmployeeInputHandler(RequestHandler):
    def post(self, *args, **kwargs):
        data = self.request.body
        # logic to process employee data