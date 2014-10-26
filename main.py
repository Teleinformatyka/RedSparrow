
import zmq
from zmq.eventloop import ioloop
ioloop.install()


import tornado
import tornado.web

import argparse
import logging
import os
import json

import tornado.web
from tornado.ioloop import IOLoop
from tornado_json.routes import get_routes
from tornado_json.application import Application


from redsparrow.config import Config
import redsparrow.api as RedSparrowApi
from redsparrow.queue import PubQueue, SubQueue, QueueMessage
from redsparrow.database.adb import Database
from redsparrow.model import Manager

from redsparrow.methods import Router, GetText


config = Config()
config.load('./config/config.yml')


class RedSparrow(tornado.web.Application):


    def __init__(self, routes, settings, db_conn=None):
        # Generate API Documentation

        # Unless gzip was specifically set to False in settings, enable it
        if "gzip" not in list(settings.keys()):
            settings["gzip"] = True

        self.db_conn = db_conn
        self.sub = SubQueue(config['subqueue'], self.on_data)
        self.pub = PubQueue(config['pubqueue'])
        self.enitity = Manager(self.db_conn)
        self.router = Router(self)
        self.router.add_method(GetText)
        tornado.web.Application.__init__(
            self,
            routes,
            **settings
        )


    def on_data(self, data):
        req = QueueMessage().from_json(data[0].decode("UTF-8"))
        self.router.find_method(req)







if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="RedSparrow  - Command Line Interface")
    parser.add_argument("--port", action="store", help="listen port ", default=8000)
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG)
    logging.info('RedSparrow listen on %s' % args.port)

    routes = get_routes(RedSparrowApi)
    logging.info("Routes\n======\n\n" + json.dumps(
        [(url, repr(rh)) for url, rh in routes],
        indent=2)
    )
    db_conn = Database(driver="pymysql", database=config['database']['database'], user=config['database']['user'], password=config['database']['password'])
    application = RedSparrow(routes=routes, settings={})
    application.listen(args.port)

    IOLoop.instance().start()




