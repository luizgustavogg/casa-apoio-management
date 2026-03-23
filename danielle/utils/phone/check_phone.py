from django.core.exceptions import ValidationError
import re


def check_phone(phone: str) -> None:
    if re.sub(r'[\d]+', "", phone):
        raise ValidationError("Telefone deve conter apenas dígitos.")
    if len(phone) < 8 or len(phone) > 9:
        raise ValidationError("Telefone deve conter 8 ou 9 dígitos.")
