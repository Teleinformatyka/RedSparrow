from docx import Document
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import  TextConverter
from pdfminer.layout import LAParams
import pdfminer
import logging
import random
import string
import os

from io import BytesIO
import tornado

from redsparrow.utils import call_subprocess


def docx_to_text(path):
    doc = Document(path)
    result = ''
    for paragraph in doc.paragraphs:
        result += paragraph.text
    return result


def odt_to_text(odt):
    if isinstance(odt, str):
        result =  call_subprocess(['odt2txt', odt])
        return result[0].decode('utf-8')
    name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
    name = ''.join([name, '.odt'])
    file_path = os.path.join('/tmp', name)
    fp = open(file_path, 'wb')
    fp.write(odt)
    fp.close()
    result =  call_subprocess(['odt2txt', file_path])
    return result[0].decode('utf-8')


def doc_to_text(doc):
    if isinstance(doc, str):
        result =  call_subprocess(['antiword', doc])
        return result[0].decode('utf-8')
    name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
    name = ''.join([name, '.doc'])
    file_path = os.path.join('/tmp', name)
    fp = open(file_path, 'wb')
    fp.write(doc)
    fp.close()
    result =  call_subprocess(['antiword', file_path])
    return result[0].decode('utf-8')


def pdf_to_text(pdf):
    pagenos = set()
    maxpages = 0
    # output option
    rotation = 0
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()

    rsrcmgr = PDFResourceManager(caching=caching)
    outtype = 'text'
    retstr = BytesIO()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = pdf
    if isinstance(pdf, str):
        fp = open(pdf, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos,
                                  maxpages=maxpages,
                                  caching=caching, check_extractable=True):
        page.rotate = (page.rotate+rotation) % 360
        interpreter.process_page(page)
    fp.close()
    device.close()
    result = retstr.getvalue()
    print(result)
    return result

