import logging
import tornado

from redsparrow.database.adisp import process, async
class Router(object):

    def __init__(self, application):
        self.__application = application
        self.__methods = {}

    def add_method(self, method):
        method.application = self.__application
        logging.info('Adding {}'.format(method.name))
        self.__methods[method.name] = method

    @process
    def find_method(self, message):
        try:
            yield self.__methods[message.method](message)
        except KeyError as err:
            logging.error("Method {} not found! {}".format(message.method, err))

