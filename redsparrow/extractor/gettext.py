import os
import tornado
import logging


from redsparrow.extractor import pdf_to_text, docx_to_text, odt_to_text, doc_to_text


def get_text(file_path):
    _, ext = os.path.splitext(file_path)
    text = ''
    if ext == '.pdf':
        text = pdf_to_text(file_path)
    elif ext == '.docx':
        text = docx_to_text(file_path)
    elif ext == '.odt':
        text = odt_to_text(file_path)
    elif ext == '.doc':
        text = doc_to_text(file_path)
    else:
        logging.error('Unknown ext {}'.format(ext))
        return
    return text



