
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

from redsparrow.database.adisp import process, async

from redsparrow.config import Config
import redsparrow.api as RedSparrowApi
from redsparrow.queue import  QueueReqMessage, ReplyQueue

from redsparrow.model.orm import db

import redsparrow.methods as ZMQMethods
from redsparrow.methods.methods_doc_gen import methods_doc_gen

from redsparrow.methods import Router, GetText, Register, Login

from redsparrow.methods.router import get_methods as get_methods_zmq

config = Config()
config.load('./config/config.yml')


class RedSparrow(tornado.web.Application):


    def __init__(self, routes, zmq_methods, settings, db_conn=None):
        # Generate API Documentation

        # Unless gzip was specifically set to False in settings, enable it
        if "gzip" not in list(settings.keys()):
            settings["gzip"] = True

        self.db_conn = db_conn
        self.logger = logging.getLogger('RedSparrow')
        self.queue = ReplyQueue(config['replyqueue'], self.on_data)

        self.router = Router(self)
        self.router.add_methods(zmq_methods)
        tornado.web.Application.__init__(
            self,
            routes,
            **settings
        )
    # @process
    def on_data(self, data):
        req = QueueReqMessage(json_data=data[0].decode("UTF-8"))
        # try:
        self.router.find_method(req)
        # except Exception as err:
        #     self.logger.error('Internal error {}'.format(err))
        #     req.error = "Internal error"
        #     self.response(req)

    def send_response(self, data):
        print(str(data))
        self.queue.send_json(str(data))





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="RedSparrow  - Command Line Interface")
    parser.add_argument("--port", action="store", help="listen port ", default=8000)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    logging.info('RedSparrow listen on %s' % args.port)

    routes = get_routes(RedSparrowApi)
    zmq_methods = get_methods_zmq(ZMQMethods)
    methods_doc_gen(zmq_methods)
    logging.info("ZMQ Methods\n======\n\n" + json.dumps(
        [(zmq_m['name'], repr(zmq_m['class'])) for zmq_m in zmq_methods],
        indent=2)
    )
    logging.info("Routes\n======\n\n" + json.dumps(
        [(url, repr(rh)) for url, rh in routes],
        indent=2)
    )

    db.bind('mysql', user=config['database']['user'], passwd=config['database']['password'],
        host=config['database']['host'], db=config['database']['database'])

    db.generate_mapping(check_tables=True, create_tables=True)
    application = RedSparrow(routes=routes, zmq_methods=zmq_methods, settings={}, db_conn=db)
    application.listen(args.port)

    IOLoop.instance().start()




