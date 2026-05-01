"""
This is our unit testing module
"""


import change_text
import unittest


class TestChangeText(unittest.TestCase):

    def test_uppercase(self):
        """ This tests the uppercase function"""
        word = 'study'
        result = change_text.all_capital(word)
        self.assertEqual(result, 'STUDY')
        
    def test_title(self):
        """This tests our Title function"""
        word = 'study'
        result = change_text.make_title(word)
        self.assertEqual(result, 'Study')

if __name__ == '__main__':
    unittest.main()
