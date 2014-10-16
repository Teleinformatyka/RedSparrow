import tornado
import tornado.web

import argparse
import logging
import os
import json

from tornado_json.routes import get_routes
from tornado_json.application import Application

import api as RedSparrowApi



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
    application = Application(routes=routes, settings={})
    application.listen(args.port)

    tornado.ioloop.IOLoop.instance().start()



