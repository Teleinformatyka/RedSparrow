

class Router(object):

    def __init__(self, application):
        self.__application = application
        self.__methods = {}

    def add_method(self, method):
        method.application = self.__application
        self.__methods[method.name] = method

    def find_method(self, message):
        print(message)
        try:
            self.__methods[message.method](message)
        except KeyError:
            pass
