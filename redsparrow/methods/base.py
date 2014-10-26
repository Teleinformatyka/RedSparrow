
class BaseMethod(object):

    def __init__(self, name):
        self.__name = names
        self.__application = None
    @property
    def name(self):
        return self.__name

    @property
    def application(self):
        return self.__application

    @application.setter
    def application(self, app):
        self.__application = app
        self.logger = app.logger


    def __call__(self, params):
        raise NotImplementedError("Not implemented")
