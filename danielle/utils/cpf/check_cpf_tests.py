from utils.cpf.check_cpf import check_cpf

from django.core.exceptions import ValidationError
from django.test import TestCase


class CheckCpfTest(TestCase):
    def test_return_none_if_cpf_is_valid(self):
        cpf = '67051060007'
        self.assertIsNone(check_cpf(cpf))

    def test_raise_error_if_cpf_is_invalid(self):
        cpf = '67053060007'
        with self.assertRaises(ValidationError):
            check_cpf(cpf)

    def test_raise_error_if_less_than_eleven_digits_in_cpf(self):
        cpf = "6705106000"
        with self.assertRaises(ValidationError):
            check_cpf(cpf)

    def test_raise_error_if_non_digits_in_cpf(self):
        cpf = "67051O60007"
        with self.assertRaises(ValidationError):
            check_cpf(cpf)
