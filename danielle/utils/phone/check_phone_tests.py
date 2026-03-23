from utils.phone.check_phone import check_phone

from django.core.exceptions import ValidationError
from django.test import TestCase


class CheckPhoneTest(TestCase):
    def test_return_none_if_phone_is_valid_with_eight_digits(self):
        phone = '90980987'
        self.assertIsNone(check_phone(phone))

    def test_return_none_if_phone_is_valid_with_nine_digits(self):
        phone = '909890987'
        self.assertIsNone(check_phone(phone))

    def test_raise_error_if_phone_has_less_than_eight_digits(self):
        phone = '6705306'
        with self.assertRaises(ValidationError):
            check_phone(phone)

    def test_raise_error_if_phone_has_more_than_nine_digits(self):
        phone = '67053061231'
        with self.assertRaises(ValidationError):
            check_phone(phone)

    def test_raise_error_if_phone_has_non_digits(self):
        phone = '67053O61'
        with self.assertRaises(ValidationError):
            check_phone(phone)
