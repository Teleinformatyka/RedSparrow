import os
import tornado

from redsparrow.extractor import pdf_to_text, docx_to_text
from redsparrow.model import Document


from .base import BaseMethod

class GetText(BaseMethod):

    def __init__(self):
        super().__init__('gettext')

    def __call__(self, message):
        file_path = message.params['file_path']
        _, ext = os.path.splitext(file_path)
        text = ''
        if ext == '.pdf':
            text = pdf_to_text(file_path)
        elif ext == '.docx':
            text = docx_to_text(file_path)
        else:
            self.logger.error('Unknow ext {}'.format(ext))
            return

        def callback(rows):
            self.logger.info("iCallback  {}".format(rows))
            self.success()

        text = text.decode("UTF-8")
        document = Document(text=text, file_path=file_path)
        result = self.application.enitity.save(document, callback)
        self.logger.info('Inserted {} row'.format(result))


