import unittest

from redsparrow.keywords import get_keywords, get_words

class KeywordsTest(unittest.TestCase):

    def test_get_keywords(self):
        keywords = get_keywords("""Jakis drugi drugi tekst tekst a tekst nie ma wikinig smok coś misiek Miak ten ta do w o i a jak test domek z aż by jakość""", 2)
        self.assertEqual(keywords,['tekst', 'drugi'])
