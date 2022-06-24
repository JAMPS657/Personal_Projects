import unittest
import CDC_draft
import argparse


import pandas as pd


class TestCDC(unittest.TestCase):
    def test_init_(self):
        ''' The method tests if data types of attributes in the class "CDC" are the correct datatype.'''
        a1 = CDC_draft.CDC(1, 2, 3, 4, 5)
        self.assertEqual("1", a1.county)
        self.assertEqual(2.0, a1.date)
        self.assertEqual(3, a1.first_dose)
        self.assertEqual(4, a1.completed)
        self.assertEqual(5, a1.booster)



    #def test_read_file(self):
        #expected = CDPHE.read_file()
        #actual = CDPHE.read_file(str())
        #self.assertEqual(expected, actual)

    #def test_agg_file(self):
        #f_inc = CDPHE.CDPHE_data
        #df1 = pd.DataFrame({'a': [f_inc]})
        #expected = pd.Series([f_inc])
        #pd.testing.assert_series_equal((df1['a']), expected, check_names=False)

    #def test_agg_file2(self):
        #f_edu = CDPHE.CDPHE_data
        #df1 = pd.DataFrame({'b': [f_edu]})
        #expected = pd.Series([f_edu])
        #pd.testing.assert_series_equal((df1['b']), expected, check_names=False)

    #def test_load_data(self):
        #lst = CDPHE.CDPHE_data.load_data()
        #expected = lst(int())
        #actual = lst(int())
        #self.assertEqual(expected, actual)

class TestCDC_data(unittest.TestCase):
    def test_init_(self):
        ''' The method tests whether or not the empty list for data is generated as a string representation
        is generated within the class "CDC_Data"
        '''
        lst = CDC_draft.CDC_Data
        expected = CDC_draft.__init__(str(lst))
        actual = CDC_draft.__init__(str(lst))
        self.assertEqual(expected, actual)

    def test_iter_(self):
        '''The method tests whether or not the data set created in the class "CDC_Data"
        is iterable.
        '''
        iter(CDC_draft.CDC_Data())

    def test_clean_data(self):
        '''The method tests whethor or not the correct data file in the "CDC_Data" for data
        cleaning is present in  the virtual environment.
        '''
        f_cov = CDC_draft.CDC_Data
        df1 = pd.DataFrame({'a': [f_cov]})
        expected = pd.Series([f_cov])
        pd.testing.assert_series_equal((df1['a']), expected, check_names=False)




if __name__ == '__main__':
    unittest.main()












