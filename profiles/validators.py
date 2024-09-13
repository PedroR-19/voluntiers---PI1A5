from django.core.exceptions   import ValidationError
from django.utils.translation import gettext_lazy as _

from validate_docbr import CPF, CNPJ


def validate_cpf(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError(_('Invalid CPF'))

def validate_cnpj(value):
    cnpj = CNPJ()
    if not cnpj.validate(value):
        raise ValidationError(_('Invalid CNPJ'))
