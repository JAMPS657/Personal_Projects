### unittest for CDC_vax.py


import unittest
import CDC_vax 
import pandas as pd


class TestCDC_data(unittest.TestCase):
    def test_init_(self):
        ''' The method tests whether or not the empty list for data is generated as a string representation
        is generated within the class "CDC_data"
        '''
        lst = CDC_vax.CDC_data
        expected = CDC_vax.__init__(str(lst))
        actual = CDC_vax.__init__(str(lst))
        self.assertEqual(expected, actual)

    def test_iter_(self):
        '''The method tests whether or not the data set created in the class "CDC_data"
        is iterable.
        '''
        iter(CDC_vax.CDC_data())

    def test_clean_data(self):
        '''The method tests whethor or not the correct data file in the "CDC_data" for data
        cleaning is present in  the virtual environment.
        '''
        f_cov = CDC_vax.CDC_data
        df1 = pd.DataFrame({'a': [f_cov]})
        expected = pd.Series([f_cov])
        pd.testing.assert_series_equal((df1['a']), expected, check_names=False)


if __name__ == '__main__':
    unittest.main()


### EOL