import tornado

from tornado_json.requesthandlers import APIHandler
from tornado_json import schema



class ConvertToTextHandler(APIHandler):

    @tornado.gen.coroutine
    def post(self, body):
        self.success('test')

    @tornado.gen.coroutine
    def get(self):
        self.success('ok')
