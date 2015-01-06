import json
import random
import copy

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
        self.socket.SNDTIMEO = 5000
        self.socket.RCVTIMEO = 5000
        self.stream = ZMQStream(self.socket, ioloop)
        self.stream.on_recv(callback)
        self.stream.flush()

    def __getattr__(self, name):
        return getattr(self.stream, name)

class RequestQueue(BaseQueue):

    def __init__(self, connect, ioloop=None):
        super().__init__(zmq.REQ)
        self.socket.connect(connect)
        self.socket.SNDTIMEO = 5000
        self.socket.RCVTIMEO = 5000
        self.stream = ZMQStream(self.socket, ioloop)
        self.stream.flush()

    def __getattr__(self, name):
        return getattr(self.stream, name)


class QueueReqMessage(object):
    """JsonRPC like reqeust message"""

    def __init__(self,id=None, params=None, method=None, json_data=None):
        if id is None:
            id = random.randint(1, 20000)
        self.id = id
        self.method = method
        if params is None:
            params = {}
        self.params = params
        if json_data:
            self.from_json(json_data)

    def from_json(self, json_data):
        data = json.loads(json_data)
        for name, value in data.items():
            self.__dict__[name] = value

        return self

    def __str__(self):
        return json.dumps(self.__dict__)



class QueueRepMessage(object):

    def __init__(self,id=None, error=None, result=None, json_data=None):
        if id is None:
            id = random.randint(1, 20000)
        self.id = id
        self.error = error
        self.result = result

    def from_json(self, json_data):
        data = json.loads(json_data)
        for name, value in data.items():
            self[name] = value
        return self

    def __str__(self):
        return json.dumps(self.__dict__)

    @property
    def success(self):
        return self.result

    @success.setter
    def success(self, message):
        self.error = None
        self.result = message

