import os
import unittest

from abvdget import CognateParser

class TestCognateParser(unittest.TestCase):
    
    def test_simple(self):
        self.assertEqual(CognateParser().parse_cognate('1'), [1])
        self.assertEqual(CognateParser().parse_cognate('10'), [10])
        self.assertEqual(CognateParser().parse_cognate('100'), [100])
        self.assertEqual(CognateParser().parse_cognate('111'), [111])
    
    def test_subset(self):
        self.assertEqual(CognateParser().parse_cognate('1,2'), [1, 2])
        self.assertEqual(CognateParser().parse_cognate('1   ,   2'), [1, 2])
        self.assertEqual(CognateParser().parse_cognate('1,2,3,4,5'), [1, 2, 3, 4, 5])
        self.assertEqual(CognateParser().parse_cognate('1, 17, 37'), [1, 17, 37])
        self.assertEqual(CognateParser().parse_cognate('1,10,66,67'), [1, 10, 66, 67])
    
    def test_dubious(self):
        self.assertEqual(CognateParser().parse_cognate('1?'), ['u_1'])
        self.assertEqual(CognateParser().parse_cognate('?'), ['u_1'])
        
    def test_dubious_subset(self):
        self.assertEqual(CognateParser().parse_cognate('1, 2?'), [1])
        self.assertEqual(CognateParser().parse_cognate('1?, 2'), [2])
        self.assertEqual(CognateParser().parse_cognate('91?, 42'), [42])
        self.assertEqual(CognateParser().parse_cognate('?, 31'), [31])
        # note that both of these are dubious, should become a unique 
        # state instead
        self.assertEqual(CognateParser().parse_cognate('1?, 2?'), ['u_1'])
    
    def test_bad_entries(self):
        # coded as x
        self.assertEqual(CognateParser().parse_cognate('X'), [])
        self.assertEqual(CognateParser().parse_cognate('x'), [])
    
    def test_s_entries(self):
        # entries that are in the wrong word (e.g. you sg. not you pl.)
        self.assertEqual(CognateParser().parse_cognate('s'), [])
    
    def test_add_unique(self):
        CP = CognateParser()
        self.assertEqual(CP.parse_cognate(''), ['u_1'])
        self.assertEqual(CP.parse_cognate(''), ['u_2'])
        self.assertEqual(CP.parse_cognate(''), ['u_3'])
        self.assertEqual(CP.parse_cognate(''), ['u_4'])

    def test_no_uniques(self):
        CP = CognateParser(uniques=False)
        self.assertEqual(CP.parse_cognate(''), [None])
        self.assertEqual(CP.parse_cognate(''), [None])
        self.assertEqual(CP.parse_cognate(''), [None])
    
    def test_dubious_with_no_strict(self):
        self.assertEqual(CognateParser().parse_cognate('1?', strict=False), [1])
    
    def test_null(self):
        self.assertEqual(CognateParser().parse_cognate(None), ['u_1'])

    def test_bad_cog_alphabetical(self):
        with self.assertRaises(ValueError):
            CognateParser().parse_cognate('A')

    def test_bad_cog_int(self):
        with self.assertRaises(ValueError):
            CognateParser().parse_cognate(1)


if __name__ == '__main__':
    unittest.main()


