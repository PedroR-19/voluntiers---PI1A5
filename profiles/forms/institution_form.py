from django                   import forms
from django.utils.translation import gettext_lazy as _
from profiles.models import Institution
import re
from django.core.exceptions import ValidationError



def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )


class InstitutionForm(forms.ModelForm):
    email            = forms.EmailField()
    password         = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label=_("Confirm password"))

    class Meta:
        model  = Institution
        fields = ['name', 'cnpj', 'email', 'state', 'city', 'logradouro', 'password', 'confirm_password']

    def clean(self):
        cleaned_data     = super().clean()
        password         = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords must match.')
        
        strong_password(password)
        
        return cleaned_data
