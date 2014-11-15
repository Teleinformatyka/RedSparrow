import json
import re
from io import StringIO
import os

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


class QueueMessage(object):

    HEADER_PID_SIZE = 2  # 10-99
    HEADER_LEN_SIZE = 8 # maximum 99999999 bytes = 95~ MB
    #  Packet ID in header
    PID_FIRST     = 10
    PID_INFO      = 10
    PID_PING      = 11
    PID_PONG      = 12
    PID_ENCAP     = 13 # Encapsulated packet *

    #  Packets related to the paper itself *
    PID_PFILE     = 40
    PID_PUSER     = 41
    PID_PAUTHOR   = 42
    PID_PTIME     = 43
    # Add new pids here */

    PID_ERROR     = 97 #  Server response
    PID_ALLOK     = 98 # Server response
    PID_REPLY     = 99 # Request for a response which should be either PID_ERROR or PID_ALLOK
    PID_LAST      = 99


    def __init__(self, msg=None):
        self.buf = StringIO()
        if msg:
            self.buf = msg


    def __str__(self):
        return self.buf.getvalue()

    def __add_header(self, msg_type, length=0):
        self.buf.write(str(msg_type).rjust(QueueMessage.HEADER_PID_SIZE, '0'))
        self.buf.write(str(length).rjust(QueueMessage.HEADER_LEN_SIZE, '0'))

    def __add_message(self, msg):
        self.buf.write(msg)

    def get_header(self):
        # wrong msg.get_message
        self.buf.seek(0, os.SEEK_END)
        if self.buf.tell() < QueueMessage.HEADER_PID_SIZE + QueueMessage.HEADER_LEN_SIZE:
            return False
        header = {}
        self.buf.seek(0)
        header_str = self.buf.read(QueueMessage.HEADER_PID_SIZE + QueueMessage.HEADER_LEN_SIZE)
        regexp = re.compile(r'([1-9][0-9]{1})').findall(header_str)
        header['type' ] = int(regexp[0])
        header['length'] = int(regexp[1])
        return header

    def get_message(self):
        header = self.get_header()
        self.buf.seek(QueueMessage.HEADER_PID_SIZE + QueueMessage.HEADER_LEN_SIZE, os.SEEK_SET)
        return self.buf.read(header['length'])

    def attach(self, msg_type, msg=None):
        if msg_type < QueueMessage.PID_FIRST or msg_type > QueueMessage.PID_LAST:
            return False
        if msg:
            self.__add_header(msg_type, len(msg))
            self.__add_message(msg)
        else:
            self.__add_header(msg_type)
        return True

    def encapsulate(self, obj):
        return self.attach(QueueMessage.PID_ENCAP, str(obj))




