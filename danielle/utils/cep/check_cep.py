from django.core.exceptions import ValidationError
import re


def check_cep(cep: str) -> None:
    if re.sub(r'[\d]+', "", cep):
        raise ValidationError("CEP deve conter apenas dígitos.")
    if len(cep) != 8:
        raise ValidationError("CEP deve conter exatamente 8 dígitos.")
