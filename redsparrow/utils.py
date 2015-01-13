from __future__ import print_function
from tornado.gen import Task, Return, coroutine
import tornado.process
import subprocess
from tornado.ioloop import IOLoop
from queue import Queue

STREAM = tornado.process.Subprocess.STREAM


# # TODO get return code
# @coroutine
# def call_subprocess(cmd, stdin_data=None):
#     """
#     Wrapper around subprocess call using Tornado's Subprocess class.
#     """
#     try:
#         sprocess = tornado.process.Subprocess(
#             cmd,
#             stdin=subprocess.PIPE,
#             stdout=STREAM,
#             stderr=STREAM
#         )
#     except OSError as e:
#         raise Return((None, e))
#
#     if stdin_data:
#         sprocess.stdin.write(stdin_data)
#         sprocess.stdin.flush()
#         sprocess.stdin.close()
#
#     result, error = yield [
#         Task(sprocess.stdout.read_until_close),
#         Task(sprocess.stderr.read_until_close)
#     ]
#
#     raise Return((result, error))
# # @coroutine
def call_subprocess(cmd, stdin_data=None):
    result = subprocess.check_output(cmd), None
    return result




class Singleton(type):
    """ Class for making Singleton object """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ListBase(object):
    """ Class for creating list/dict like object.
    Magic method are implemented.
    """

    @property
    def data(self):
        """Basic property getter"""
        raise NotImplementedError()

    @data.setter
    def data(self, value):
        """Basic property setter"""
        raise NotImplementedError()

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def __delitem__(self, key):
        del self.data[key]

    def __len__(self):
        return len(self.data)

