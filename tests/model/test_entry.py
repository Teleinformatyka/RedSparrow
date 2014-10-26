
import unittest
import json

from redsparrow.model import Document

class DocumentTest(unittest.TestCase):

    def test_str_method(self):
        doc = Document(11, "test", "dobre.pdf")
        expect = json.loads("{\"id\": 11, \"file_path\": \"dobre.pdf\", \"text\": \"test\"}")

        self.assertEqual(json.loads(str(doc)), expect)

    def test_insert_method(self):
        doc = Document(11, "test", "dobre.pdf")
        result = doc.insert()
        self.assertTrue("INSERT" in result[0])
        self.assertTrue( result[1][0] in ("test","dobre.pdf"))

