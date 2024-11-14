from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import requests
from validate_docbr import CPF, CNPJ
import re

def validate_cpf(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError(_('Invalid CPF'))

def validate_cnpj(value):
    cnpj = CNPJ()
    if not cnpj.validate(value):
        raise ValidationError(_('Invalid CNPJ'))
   
def validate_password_strength(value):
    if value is None:
        raise ValidationError(_('Password cannot be empty.'))
    if len(value) < 8:
        raise ValidationError(_('Password must be at least 8 characters long.'))
    if not re.search(r'[A-Z]', value):
        raise ValidationError(_('Password must contain at least one uppercase letter.'))
    if not re.search(r'[a-z]', value):
        raise ValidationError(_('Password must contain at least one lowercase letter.'))
    if not re.search(r'[0-9]', value):
        raise ValidationError(_('Password must contain at least one digit.'))
    if not re.search(r'[^a-zA-Z0-9]', value):
        raise ValidationError(_('Password must contain at least one special character.'))


def validate_email(email):
    api_key = "bb5012362a7542feb491bb6b8994ea37"
    url = f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        is_valid_format = data.get('is_valid_format', {}).get('value', False)
        is_smtp_valid = data.get('is_smtp_valid', {}).get('value', False)

        if is_valid_format and is_smtp_valid:
            return  
        
        raise ValidationError(_('Invalid email address. Please enter a valid email.'))

    except requests.exceptions.RequestException:
        raise ValidationError(_('Error validating email address. Please try again later.'))
    except KeyError:
        raise ValidationError(_('Unexpected response format from the email validation service.'))
