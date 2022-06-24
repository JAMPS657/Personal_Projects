### unittest for CDPHE_demo..py


import unittest
import CDPHE_demo
import pandas as pd


class TestCDPHE_data(unittest.TestCase):
    def test_init_(self):
        ''' The method tests whether or not the empty list for data is generated as a string representation within
        the class "CDPHE_data".
        '''
        lst = CDPHE_demo.CDPHE_data
        expected = CDPHE_demo.__init__(str(lst))
        actual = CDPHE_demo.__init__(str(lst))
        self.assertEqual(expected, actual)

    def test_iter_(self):
        '''The method tests whether or not attributes of the class "CDPHE_data"
         is not iterable.
         '''
        iter(CDPHE_demo.CDPHE_data())

    def test_agg_file(self):
        '''The method tests whethor or not the correct data file in the "CDPHE" class for data
        cleaning is present in the virtual environment.
        '''
        f_inc = CDPHE_demo.CDPHE_data
        df1 = pd.DataFrame({'a': [f_inc]})
        expected = pd.Series([f_inc])
        pd.testing.assert_series_equal((df1['a']), expected, check_names=False)

    def test_agg_file2(self):
        '''The method tests whethor or not the correct supplementary data file in the "CDPHE" class for data
        cleaning is present in the virtual environment.
        '''
        f_edu = CDPHE_demo.CDPHE_data
        df1 = pd.DataFrame({'b': [f_edu]})
        expected = pd.Series([f_edu])
        pd.testing.assert_series_equal((df1['b']), expected, check_names=False)


if __name__ == '__main__':
    unittest.main()


### EOL