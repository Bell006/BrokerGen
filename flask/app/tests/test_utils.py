import unittest

from ..utils import *

class TestCase_format_number(unittest.TestCase):
    def test_format_valid_number_mobile(self):
        self.assertEqual(format_phone_number("62988888888"), "(62) 9 8888-8888")

    def test_format_valid_number_landline(self):
        self.assertEqual(format_phone_number("3423423432"), "(34) 2342-3432")
    
    def test_format_number_with_non_digits(self):
        self.assertEqual(format_phone_number("(34) 9-2342-3432"), "(34) 9 2342-3432")

    def test_format_number_with_leading_zero(self):
        self.assertEqual(format_phone_number("03423423432"), "(34) 2342-3432")

    def test_format_invalid_number(self):
        with self.assertRaises(AppError):
            format_phone_number("")

class TestCase_get_state_abbreviation(unittest.TestCase):
    def test_valid_state(self):
        self.assertEqual(get_state_abbreviation('São Paulo'), 'SP')
    
    def test_invalid_state(self):
        with self.assertRaises(AppError):
            get_state_abbreviation('Batata')

class TestCase_validate_name(unittest.TestCase):
    def test_valid_name(self):
        self.assertTrue
    
    def test_invalid_name(self):
        with self.assertRaises(AppError):
            validate_name('Bell da Silva Pereira')
    




if __name__ == '__main__':
    unittest.main()