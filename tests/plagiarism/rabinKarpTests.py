import unittest
from RabinKarbAlgorithm import RabinKarbAlgorithm
from testClass import testClass
class Test_rabinKarpTests(unittest.TestCase):
    def setUp(self):
        self.test = RabinKarbAlgorithm()
        self.arrayTest = [testClass("aaaaaaaaaaaaaassss", "sss", [14, 15]),
                          testClass("lalka", "barbie", -1),
                          testClass("maja pszcz", "pszcz", [5]),
                          testClass("a", "papuga", -1)]

    def testwhen_test_failed(self):     
        self.assertEqual(self.test.Calculate("aaaaaaaaaaaaaassss", "sss", 257, 13), self.arrayTest[1].result)
    def testwhen_test_success(self):
        self.test = RabinKarbAlgorithm()
        self.assertEqual(self.test.Calculate("aaaaaaaaaaaaaassss", "sss", 257, 13), self.arrayTest[0].result)
    def testwhen_input_text_too_short(self):
        self.test = RabinKarbAlgorithm()
        self.assertEqual(self.test.Calculate("a", "papuga", 257, 13), self.arrayTest[3].result)
    def testwhen_input_text_is_none(self):
        self.test = RabinKarbAlgorithm()
        self.assertEqual(self.test.Calculate(None, "papuga", 257, 13), -1)
    def testwhen_input_pattern_and_text_is_none(self):
        self.test = RabinKarbAlgorithm()
        self.assertEqual(self.test.Calculate(None, None, 257, 13), -1)
    def testwhen_input_pattern_is_none(self):
        self.test = RabinKarbAlgorithm()
        self.assertEqual(self.test.Calculate("maja", None, 257, 13),-1)
    def testwhen_input_pattern_and_text_is_empty(self):
        self.test = RabinKarbAlgorithm()
        self.assertEqual(self.test.Calculate("", "", 257, 13), -1)
    def testwhen_input_pattern_is_empty(self):
        self.test = RabinKarbAlgorithm()
        self.assertEqual(self.test.Calculate("asdwwqw", "", 257, 13), -1)
    def testwhen_input_text_is_empty(self):
        self.test = RabinKarbAlgorithm()
        self.assertEqual(self.test.Calculate("", "xxxw", 257, 13), -1)

if __name__ == '__main__':
    unittest.main()
