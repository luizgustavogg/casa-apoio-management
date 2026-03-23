from django.core.exceptions import ValidationError
import re


def check_cpf(cpf: str) -> None:
    if re.sub(r'[\d]+', "", cpf):
        raise ValidationError("CPF deve conter apenas dígitos de 0 a 9.")
    if len(cpf) != 11:
        raise ValidationError("CPF deve ter 11 dígitos.")

    d1 = ((sum([int(a) * b
                for a, b in zip(cpf[:-2], list(range(10, 1, -1)))]) * 10) %
          11) % 10
    d2 = (
        (sum([int(a) * b
              for a, b in zip(cpf[:-2], list(range(11, 2, -1)))] + [d1 * 2]) *
         10) % 11) % 10
    if not (str(d1) == cpf[-2] and str(d2) == cpf[-1]):
        raise ValidationError("CPF inválido.")
