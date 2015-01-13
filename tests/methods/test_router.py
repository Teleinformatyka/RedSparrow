import unittest
from unittest.mock import MagicMock, patch, Mock

from redsparrow.methods.router import Router
from redsparrow.queue import  QueueReqMessage

class RouterTest(unittest.TestCase):


    def setUp(self):
        self.method = MagicMock('method');
        self.method.process = MagicMock('method_process')
        self.method.fajna = MagicMock('method_fajna')
        self.method.name = 'metoda'


    def test_routing_call_process(self):
        router = Router(MagicMock('application'))
        router.add_method('metoda', MagicMock(return_value=self.method))
        message = QueueReqMessage()
        message.method = 'metoda'
        message.params = {'key': 'test'}
        router.find_method(message)
        self.method.process.assert_called_with(key='test')

    def test_routing_call_fajna(self):
        application = MagicMock('application')
        application.send_response = MagicMock('application.send_response')

        router = Router(application)
        router.add_methods([{'class': MagicMock(return_value=self.method), 'name': 'fajna', 'original_name': 'fajna'}])
        message = QueueReqMessage()
        message.method = 'fajna'
        message.params = {'key': 'test'}
        router.find_method(message)
        application.send_response.assert_called_with
        self.assertFalse(application.send_response.called)
        self.assertFalse(self.method.process.called)
        self.method.fajna.assert_called_with(key='test')
