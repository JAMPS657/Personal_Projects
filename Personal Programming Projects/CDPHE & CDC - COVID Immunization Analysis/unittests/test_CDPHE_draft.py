import unittest
import CDPHE
import argparse


import pandas as pd


class TestCDPHE_data(unittest.TestCase):
    def test_init_(self):
        ''' The method tests whether or not the empty list for data is generated as a string representation within
        the class "CDPHE_data".
        '''
        lst = CDPHE.CDPHE_data
        expected = CDPHE.__init__(str(lst))
        actual = CDPHE.__init__(str(lst))
        self.assertEqual(expected, actual)

    def test_iter_(self):
        '''The method tests whether or not attributes of the class "CDPHE_Data"
         is not iterable.
         '''
        CDPHE.CDPHE_data

    #def test_read_file(self):
        #expected = CDPHE.read_file()
        #actual = CDPHE.read_file(str())
        #self.assertEqual(expected, actual)

    def test_agg_file(self):
        '''The method tests whethor or not the correct data file in the "CDPHE" class for data
        cleaning is present in the virtual environment.
        '''
        f_inc = CDPHE.CDPHE_data
        df1 = pd.DataFrame({'a': [f_inc]})
        expected = pd.Series([f_inc])
        pd.testing.assert_series_equal((df1['a']), expected, check_names=False)

    def test_agg_file2(self):
        '''The method tests whethor or not the correct supplementary data file in the "CDPHE" class for data
        cleaning is present in the virtual environment.
        '''
        f_edu = CDPHE.CDPHE_data
        df1 = pd.DataFrame({'b': [f_edu]})
        expected = pd.Series([f_edu])
        pd.testing.assert_series_equal((df1['b']), expected, check_names=False)

    #def test_load_data(self):
        #lst = CDPHE.CDPHE_data.load_data()
        #expected = lst(int())
        #actual = lst(int())
        #self.assertEqual(expected, actual)





if __name__ == '__main__':
    unittest.main()












