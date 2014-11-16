import os
from tornado.testing import AsyncTestCase, gen_test

from redsparrow.extractor import doc_to_text, docx_to_text, odt_to_text

DATA_PATH = 'lecturer_database'
class ExtratorNotUnitTest(AsyncTestCase):
    DOC_FILE = os.path.join(DATA_PATH, 'Zmiany w pracy dyplomowej.doc')
    DOCX_FILE = os.path.join(DATA_PATH, 'praca_mgr.docx')
    ODT_FILE = os.path.join(DATA_PATH, 'Mariusz_Starzak-praca_magisterska.odt')
    def test_pdf(self):
        pass

    @gen_test
    def test_doc(self):
        result = yield doc_to_text(ExtratorNotUnitTest.DOC_FILE)
        self.assertTrue('przetwarzane' in result )

    def test_docx(self):
        result = docx_to_text(ExtratorNotUnitTest.DOCX_FILE)
        self.assertTrue('admin' in result )

    @gen_test
    def test_odt(self):
        result = yield odt_to_text(ExtratorNotUnitTest.ODT_FILE)
        self.assertTrue('JSONObject' in result )
