import os
import tornado

from redsparrow.extractor import pdf_to_text, docx_to_text


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



