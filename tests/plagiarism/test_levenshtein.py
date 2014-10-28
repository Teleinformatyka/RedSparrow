import unittest


import redsparrow.plagiarism.levenshtein as Levenshtein

class TestClass(unittest.TestCase):

    def test_zero_distance(self):
        self.assertEquals(Levenshtein.distance('test', 'test'), 0)

    def test_not_zero_distance(self):
        self.assertEquals(Levenshtein.distance('test11', 'test'), 2)
