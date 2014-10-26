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
        print(ZMQStream)
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


class QueueMessage(object):

    def __init__(self, id=None, method=None,  params=None):
        self.id = id
        self.method = method
        self.params = params

    def from_json(self, json_data):
        data = json.loads(json_data)
        self.params = data['params']
        self.id = data['id']
        self.method = data['method']
        return self

    def __str__(self):
        return json.dumps(self.__dict__)

