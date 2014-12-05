import unittest

from unittest.mock import MagicMock, patch, Mock
from redsparrow.methods import GetText
from redsparrow.queue import QueueReqMessage


class GetTextTest(unittest.TestCase):


    def test_name(self):
        method = GetText()
        self.assertEqual('gettext', method.name)

    def setUp(self):
        self.mock_pdf = MagicMock('pdf_to_text', return_value=b"testowypdf")
        self.mock_docx = MagicMock('docx_to_text', return_value=b"testowydocx")

        self.mock_application = MagicMock('application')

        self.patch_pdf = patch('redsparrow.methods.gettext.pdf_to_text', self.mock_pdf).start()
        self.patch_docx = patch('redsparrow.methods.gettext.docx_to_text', self.mock_docx).start()

        self.mock_application.logger = MagicMock('application.logger')
        self.mock_application.logger.error = MagicMock('application.logger')
        self.mock_application.logger.info = MagicMock('application.logger')
        self.mock_application.enitity = MagicMock('application.EntityManager')
        self.mock_application.enitity.save = MagicMock('EntityManager.save')


    # def test_call_unknow_ext(self):
    #     """Test get text when no extension given"""
    #     method = GetText()
    #     msg = QueueReqMessage()
    #     msg.params = {}
    #     msg.params['file_path'] = '/tmp/test'
    #     method.application = self.mock_application
    #     method(msg)
    #     self.assertTrue(self.mock_application.logger.error.called)
    #
    # def test_call_pdf(self):
    #     """Test get text when pdf given"""
    #     method = GetText()
    #     msg = QueueReqMessage()
    #     msg.params = {}
    #     msg.params['file_path'] = '/tmp/test.pdf'
    #     method.application = self.mock_application
    #     method(msg)
    #     self.assertFalse(self.mock_application.logger.error.called)
    #     self.mock_pdf.assert_called_with('/tmp/test.pdf')
    #     self.assertTrue(self.mock_application.enitity.save.called)
    #
    # def test_call_docx(self):
    #     """Test get text when docx given"""
    #     method = GetText()
    #     msg = QueueReqMessage()
    #     msg.params = {}
    #     msg.params['file_path'] = '/tmp/test.docx'
    #     method.application = self.mock_application
    #     method(msg)
    #     self.assertFalse(self.mock_application.logger.error.called)
    #     self.mock_docx.assert_called_with('/tmp/test.docx')
    #     self.assertTrue(self.mock_application.enitity.save.called)




