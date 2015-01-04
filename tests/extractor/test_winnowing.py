import unittest

from redsparrow.extractor import winnow, winnow_all


class WinnowingTest(unittest.TestCase):


    def test_winnowing_all_same_text(self):
        winnowed = winnow_all("""Tekst krotki""")
        winnowed_same = winnow_all("""Tekst krotki""")
        self.assertEqual(winnowed, winnowed_same)
        # self.assertEqual(winnowed, [])


    def test_winnowing(self):
        actual = winnow('A do run run run, a do run run')
        expected = {5: 23942, 14: 2887, 2: 1966, 9: 23942, 20: 1966}
        self.assertEqual(actual, expected)

    def test_winnowing_all_diffrent_text(self):
        winnowed = winnow_all("""Tekt krotki""")
        winnowed1 = winnow_all("""Tekst krotki""")
        self.assertNotEqual(winnowed, winnowed1)
