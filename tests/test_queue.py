import unittest
from unittest.mock import MagicMock, patch, Mock

from redsparrow.queue import BaseQueue, PubQueue, SubQueue, QueueReqMessage


class BaseQueueTest(unittest.TestCase):

    def setUp(self):
        self.mock_ctx = MagicMock('zmq.Ctx')
        self.mock_socket = Mock('Socket')
        self.mock_ctx.socket = self.mock_socket
        self.mock_ctx.return_value = self.mock_ctx
        self.patch_ctx = patch('zmq.Context.instance', self.mock_ctx)
        self.patch_ctx.start()

    def tearDown(self):
        self.patch_ctx.stop()

    def test_construct(self):
        base = BaseQueue('test')
        self.mock_socket.assert_called_with('test')




class PubQueueTest(unittest.TestCase):

    def setUp(self):
        self.mock_ctx = MagicMock('zmq.Ctx')

        self.mock_socket = MagicMock('Socket')
        self.mock_socket.bind = MagicMock('Socket.bind')

        mock_socket = MagicMock('Socket', return_value=self.mock_socket)
        self.mock_ctx.socket = mock_socket
        self.mock_ctx.return_value = self.mock_ctx
        self.patch_ctx = patch('zmq.Context.instance', self.mock_ctx)
        self.patch_ctx.start()

        self.mock_zmqstream = MagicMock('ZMQStream')
        self.patch_zmqstream = patch('redsparrow.queue.ZMQStream', self.mock_zmqstream)
        self.patch_zmqstream.start()


    def tearDown(self):
        self.patch_ctx.stop()
        self.patch_zmqstream.stop()

    def test_construct(self):
        oub  = PubQueue('test')
        self.mock_socket.bind.assert_called_with('test')
        self.mock_zmqstream.assert_called_with(self.mock_socket, None)

class SubQueueTest(unittest.TestCase):

    def setUp(self):
        self.mock_ctx = MagicMock('zmq.Ctx')

        self.mock_socket = MagicMock('Socket')
        self.mock_socket.connect = MagicMock('Socket.bind')

        mock_socket = MagicMock('Socket', return_value=self.mock_socket)
        self.mock_ctx.socket = mock_socket
        self.mock_ctx.return_value = self.mock_ctx
        self.patch_ctx = patch('zmq.Context.instance', self.mock_ctx)
        self.patch_ctx.start()

        self.mock_zmqstream = MagicMock('ZMQStream')
        self.mock_zmqstream.on_recv = MagicMock('on_recv')
        self.mock_zmqstream.flush = MagicMock('flush')
        self.mock_zmqstream.return_value = self.mock_zmqstream
        self.patch_zmqstream = patch('redsparrow.queue.ZMQStream', self.mock_zmqstream)
        self.patch_zmqstream.start()


    def tearDown(self):
        self.patch_ctx.stop()
        self.patch_zmqstream.stop()

    def test_construct(self):
        callback = Mock('callback')
        oub  = SubQueue('test', callback)
        self.mock_socket.connect.assert_called_with('test')
        self.mock_zmqstream.assert_called_with(self.mock_socket, None)
        self.mock_zmqstream.on_recv.assert_called_with(callback)


class QueueReqMessageTest(unittest.TestCase):

    def test_get_method(self):
        msg = QueueReqMessage(json_data="""{"method": "test"}""")
        self.assertEqual(msg.method, 'test')

    def test_get_params(self):
        msg = QueueReqMessage(json_data="""{"params": "test"}""")
        self.assertEqual(msg.params, 'test')

    def test_unique_Id(self):
        msg1 =  QueueReqMessage()
        msg2 = QueueReqMessage()
        self.assertTrue(msg1.id != msg2.id)

    def test_unique_data3(self):
        msg1 =  QueueReqMessage()
        msg2 = QueueReqMessage()
        msg1.params["ala"] = True
        msg2.params['ala'] = False
        self.assertEqual(False,  msg2.params['ala'])
        self.assertEqual(True,  msg1.params['ala'])
