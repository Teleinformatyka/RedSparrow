import unittest
import redsparrow.plagiarism.rabinkarb as RabinKarb

class Test_rabinKarpTests(unittest.TestCase):
    def setUp(self):
        self.arrayTest =  { ("aaaaaaaaaaaaaassss", "sss"):[14, 15],
                             ("lalka", "barbie"):  -1,
                             ("maja pszcz", "pszcz"): [5],
                             ("a", "papuga"): -1}

    def testwhen_test_failed(self):
        data = ("aaaaaaaaaaaaaassss", "sss")
        self.assertEqual(RabinKarb.calculate(data[0], data[1], 257, 13), self.arrayTest[data])

    def testwhen_test_success(self):
        data = ("aaaaaaaaaaaaaassss", "sss")
        self.assertEqual(RabinKarb.calculate(data[0], data[1], 257, 13), self.arrayTest[data])

    def testwhen_input_text_too_short(self):
        data = ("aaaaaaaaaaaaaassss", "sss")
        self.assertEqual(RabinKarb.calculate(data[0], data[1], 257, 13), self.arrayTest[data])

    def testwhen_input_text_is_none(self):
        self.assertEqual(RabinKarb.calculate(None, "papuga", 257, 13), -1)

    def testwhen_input_pattern_and_text_is_none(self):
        self.assertEqual(RabinKarb.calculate(None, None, 257, 13), -1)

    def testwhen_input_pattern_is_none(self):
        self.assertEqual(RabinKarb.calculate("maja", None, 257, 13),-1)

    def testwhen_input_pattern_and_text_is_empty(self):
        self.assertEqual(RabinKarb.calculate("", "", 257, 13), -1)

    def testwhen_input_pattern_is_empty(self):
        self.assertEqual(RabinKarb.calculate("asdwwqw", "", 257, 13), -1)

    def testwhen_input_text_is_empty(self):
        self.assertEqual(RabinKarb.calculate("", "xxxw", 257, 13), -1)

if __name__ == '__main__':
    unittest.main()
