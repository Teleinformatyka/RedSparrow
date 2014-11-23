from redsparrow.queue import QueueRepMessage

class BaseMethod(object):
    application = None
    def __init__(self, name):
        self._name = name
        self.__application = None
        self._response = None
        self._request = None
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def application(self):
        return self.__application

    @application.setter
    def application(self, app):
        self.__application = app
        self.logger = app.logger

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, request):
        self._request = request

    def success(self, message=None):
        if message:
            self._response.success = message
        self.application.send_response(self._response)
        self._response = None

    def error(self, message=None):
        if message:
            self._response.error = message
        self.application.send_response(self._response)
        self._response = None

    def __call__(self, *args, **kwargs):
        self._process(*args, **kwargs)

    def process(self, *args, **kwargs):
        self._response = QueueRepMessage(id=self._request.id)
        self._process(*args, **kwargs)

    def _process(self, *args, **kwargs):
        raise NotImplementedError()

