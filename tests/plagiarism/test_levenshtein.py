import unittest


from redsparrow.plagiarism.levenshtein import levenshtein_distance

class TestClass(unittest.TestCase):

    def test_zero_distance(self):
        self.assertEquals(levenshtein_distance('test', 'test'), 0)

    def test_not_zero_distance(self):
        self.assertEquals(levenshtein_distance('test11', 'test'), 2)
