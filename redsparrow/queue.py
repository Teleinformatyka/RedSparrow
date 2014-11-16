import json

import zmq
from zmq.eventloop.zmqstream import ZMQStream

class BaseQueue:
    def __init__(self, zmq_type):
        self.ctx = zmq.Context.instance()
        self.socket = self.ctx.socket(zmq_type)



class PubQueue(BaseQueue):

    def __init__(self, bind, ioloop=None):
        super().__init__(zmq.PUSH)
        self.socket.bind(bind)
        self.stream = ZMQStream(self.socket, ioloop)
        self.stream.on_send(self.__on_send)

    def __on_send(self, msq, status):
        print(msq, status)

    def send(self, data):
        self.stream.send(data)
        self.stream.flush()

    def send_string(self, data):
        self.stream.send_string(data)
        self.stream.flush()

class SubQueue(BaseQueue):

    def __init__(self, connect, callback, ioloop=None):
        super().__init__(zmq.PULL)
        self.socket.connect(connect)
        self.stream = ZMQStream(self.socket, ioloop)
        self.stream.on_recv(callback)
        self.stream.flush()


class ReplyQueue(BaseQueue):

    def __init__(self, bind, callback, ioloop=None):
        super().__init__(zmq.REP)
        self.socket.bind(bind)
        self.stream = ZMQStream(self.socket, ioloop)
        self.stream.on_recv(callback)
        self.stream.flush()

    def __getattr__(self, name):
        return getattr(self.stream, name)



class QueueMessage(object):
    """JsonRPC like message"""

    def __init__(self, json_data=None):
        self.__data = {}
        if json_data:
            self.from_json(json_data)

    def from_json(self, json_data):
        self.__data = json.loads(json_data)
        return self

    def __str__(self):
        return json.dumps(self.__data)

    def __getattr__(self, name):
        try:
            return self.__data[name]
        except KeyError:
            return None

    @property
    def method(self):
        try:
            return self.__data['method']
        except KeyError:
            return None
    @method.setter
    def method(self, value):
        self.__data['method'] = value

    @property
    def params(self):
        try:
            return self.__data['params']
        except KeyError:
            return None

    @params.setter
    def params(self, value):
        self.__data['params'] = value
