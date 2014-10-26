import os

from redsparrow.extractor import pdf_to_text, docx_to_text
from redsparrow.model import Document

from .base import BaseMethod
from redsparrow.queue import QueueMessage

class GetText(BaseMethod):

    def __init__(self):
        super().__init__('gettext')

    def __call__(self, message):
        file_path = message.params.file_path
        _, ext = os.path.splitext(file_path)
        text = ''
        if ext == 'pdf':
            text = pdf_to_text(file_path)
        elif ext == 'docx':
            text = docx_to_text(file_path)
        else:
            self.logger.error('Unknow ext')
            return


        def callback(rows):
            response = QueueMessage(message.id, message.method, rows.id)
            self.__application.pub.send_string(response)


        document = Document(text=text, file_path=file_path)
        result = self.__application.enitity.save(document, callback)


