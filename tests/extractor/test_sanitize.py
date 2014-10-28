import unittest
from redsparrow.extractor import sanitizedString


class TestSanitinze(unittest.TestCase):

    def test_special_char_and_tolower(self):
        self.assertEqual(sanitizedString('%$$##@ @  @ Ala'), 'ala')

    def test_utf8(self):
        self.assertEqual(sanitizedString('śćąążźć'), 'śćąążźć')
