from django.core.exceptions import ValidationError
from django.test import TestCase

from utils.cep.check_cep import check_cep


class CheckCepTest(TestCase):
    def test_return_none_if_valid_cep(self):
        cep = "38200125"
        self.assertIsNone(check_cep(cep))

    def test_raise_error_if_more_than_eight_digits_in_cep(self):
        cep = "123456789"
        with self.assertRaises(ValidationError):
            check_cep(cep)

    def test_raise_error_if_less_than_eight_digits_in_cep(self):
        cep = "1234567"
        with self.assertRaises(ValidationError):
            check_cep(cep)

    def test_raise_error_if_non_digits_in_cep(self):
        cep = "1234567a"
        with self.assertRaises(ValidationError):
            check_cep(cep)
