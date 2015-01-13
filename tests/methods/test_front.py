import unittest

from unittest.mock import MagicMock, patch, Mock
from redsparrow.methods.base import BaseMethod
from redsparrow.methods import Register, Login
from redsparrow.queue import QueueReqMessage, QueueReqMessage


class RegisterTest(unittest.TestCase):


    def test_name(self):
        method = Register()
        self.assertEqual('register', method.name)

    def setUp(self):
        self.mock_user = MagicMock('User')
        self.mock_user.select = MagicMock('User.select', return_value=['istnieje'])
        self.mock_user.insert = MagicMock('User.select', return_value=['istnieje'])

        self.mock_application = MagicMock('application')

        def db_session(f):
            def wrapped_f():
                f()
            return wrapped_f
        self.patch_user = patch('redsparrow.methods.front.User', self.mock_user).start()
        self.patch_db_session = patch('redsparrow.methods.front.db_session', db_session).start()


        self.mock_application.logger = MagicMock('application.logger')
        self.mock_application.logger.error = MagicMock('application.logger')
        self.mock_application.logger.info = MagicMock('application.logger')
        self.mock_application.send_response = MagicMock('application.send_response')
        BaseMethod.application = self.mock_application


    def test_user_already_exists(self):
        method = Register()
        msg = QueueReqMessage()
        msg.params = { 'login': 'test', 'password':'sha2', 'surname': 'test', 'name': 'test', 'email':'test1'}
        method.request = msg
        method.process(**msg.params)
        self.assertTrue(self.mock_user.select.called)
        self.assertFalse(self.mock_user.insert.called)
        self.assertTrue(self.mock_application.send_response.called)


    def test_user_register(self):
        method = Register()
        self.mock_user.select.return_value = []
        self.patch_user = patch('redsparrow.methods.front.User', self.mock_user).start()
        msg = QueueReqMessage()
        msg.params = { 'login': 'test', 'password':'sha2', 'surname': 'test', 'name': 'test', 'email':'test1'}
        method.request = msg
        method.process(**msg.params)
        self.assertTrue(self.mock_user.select.called)
        self.assertTrue(self.mock_user.called)
        self.assertTrue(self.mock_application.send_response.called)

class LoginTest(unittest.TestCase):
    def test_name(self):
        method = Login()
        self.assertEqual('login', method.name)

    def setUp(self):
        self.mock_user = MagicMock('User')
        self.mock_user.select = MagicMock('User.select', return_value=[MagicMock()])

        self.mock_application = MagicMock('application')
        def db_session(f):
            def wrapped_f():
                f()
            return wrapped_f
        self.patch_user = patch('redsparrow.methods.front.User', self.mock_user).start()
        self.patch_db_session = patch('redsparrow.methods.front.db_session', db_session).start()


        self.mock_application.logger = MagicMock('application.logger')
        self.mock_application.logger.error = MagicMock('application.logger')
        self.mock_application.logger.info = MagicMock('application.logger')
        self.mock_application.send_response = MagicMock('application.send_response')

        BaseMethod.application = self.mock_application

    def test_user_exists(self):
        method = Login()
        msg = QueueReqMessage()
        msg.params = { 'login': 'test', 'password':'sha2' }
        method.request = msg
        method.success = MagicMock()
        method.process(**msg.params)
        self.assertTrue(self.mock_user.select.called)
        self.assertTrue(method.success.called)


    def test_user_not_exists(self):
        method = Login()
        self.mock_user.select.return_value = []
        self.patch_user = patch('redsparrow.methods.front.User', self.mock_user).start()
        msg = QueueReqMessage()
        msg.params = { 'login': 'test', 'password':'sha2' }
        method.request = msg
        method.success = MagicMock()
        method.error = MagicMock()
        method.process(**msg.params)
        self.assertTrue(self.mock_user.select.called)
        self.assertFalse(method.success.called)
        self.assertTrue(method.error.called)


