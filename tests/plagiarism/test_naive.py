import unittest
import redsparrow.plagiarism.naive as Naive

class Test_NaiveTests(unittest.TestCase):
    def setUp(self):
        self.arrayTest =  { ("aaaaaaaaaaaaaassss", "sss"):[14, 15],
                             ("lalka", "barbie"):  -1,
                             ("maja pszcz", "pszcz"): [5],
                             ("a", "papuga"): -1}

    def testwhen_test_failed(self):
        data = ("aaaaaaaaaaaaaassss", "sss")
        self.assertEqual(Naive.calculate(data[0], data[1]), self.arrayTest[data])

    def testwhen_test_success(self):
        data = ("aaaaaaaaaaaaaassss", "sss")
        self.assertEqual(Naive.calculate(data[0], data[1]), self.arrayTest[data])

    def testwhen_input_text_too_short(self):
        data = ("aaaaaaaaaaaaaassss", "sss")
        self.assertEqual(Naive.calculate(data[0], data[1]), self.arrayTest[data])

    def testwhen_input_text_is_none(self):
        self.assertEqual(Naive.calculate(None, "papuga"), -1)

    def testwhen_input_pattern_and_text_is_none(self):
        self.assertEqual(Naive.calculate(None, None), -1)

    def testwhen_input_pattern_is_none(self):
        self.assertEqual(Naive.calculate("maja", None),-1)

    def testwhen_input_pattern_and_text_is_empty(self):
        self.assertEqual(Naive.calculate("", ""), -2)

    def testwhen_input_pattern_is_empty(self):
        self.assertEqual(Naive.calculate("asdwwqw", ""), -2)

    def testwhen_input_text_is_empty(self):
        self.assertEqual(Naive.calculate("", "xxxw"), -2)

if __name__ == '__main__':
    unittest.main()