import unittest

from redsparrow.methods import GetText


class GetTextTest(unittest.TestCase):


    def test_name(self):
        method = GetText()
        self.assertEqual('gettext', method.name)
