import logging

from redsparrow.queue import QueueRepMessage

class BaseMethod(object):
    """
        Base method class
        it helps to make rpc interface
    """
    application = None
    def __init__(self, name=None):
        if name is None:
            name = self.__class__.__name__
        self.__sended_response = False
        self._name = name
        self._response = None
        self._request = None
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val


    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, request):
        self._request = request

    def success(self, message="Ok"):
        if self.__sended_response is True:
            logging.warning("You have already send response!")
            return
        self._response = QueueRepMessage(id=self._request.id)
        self._response.success = message
        BaseMethod.application.send_response(self._response)
        self.__sended_response = True

    def error(self,  message="Error", code=-32602):

        if self.__sended_response is True:
            logging.warning("You have already send response!")
            return
        self._response = QueueRepMessage(id=self._request.id)
        self._response.error = { 'code': code, 'message': message}
        logging.error("Base/error  id={} method={} error={}".format(self._response.id, self._request.method, message))
        BaseMethod.application.send_response(self._response)
        self.__sended_response = True


    def process(self, *args, **kwargs):
        """ Method called when JSON-RPC for __name"""
        self._response = QueueRepMessage(id=self._request.id)

    def add_to_queue(self, data):
        BaseMethod.application.periodic_detector.queue.put_nowait(data)


