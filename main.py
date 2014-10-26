
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

import redsparrow.api as RedSparrowApi
from redsparrow.queue import PubQueue, SubQueue





class RedSparrow(tornado.web.Application):


    def __init__(self, routes, settings, db_conn=None):
        # Generate API Documentation

        # Unless gzip was specifically set to False in settings, enable it
        if "gzip" not in list(settings.keys()):
            settings["gzip"] = True

        self.db_conn = db_conn
        self.sub = SubQueue('tcp://127.0.0.1:5600', self.on_data)
        self.pub = PubQueue('tcp://127.0.0.1:4600')
        tornado.web.Application.__init__(
            self,
            routes,
            **settings
        )


    def on_data(self, data):
        logging.info('Data {}'.format(data))






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
    application = RedSparrow(routes=routes, settings={})
    application.listen(args.port)

    IOLoop.instance().start()




