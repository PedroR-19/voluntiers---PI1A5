from django                   import forms
from django.utils.translation import gettext_lazy as _
from profiles.models import Institution, User
import re
from django.core.exceptions import ValidationError
from profiles.validators import validate_password_strength, validate_email


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
    email = forms.EmailField(
        # validators=[validate_email],
        label=_("Email")
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_("Password"),
        validators=[validate_password_strength]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_("Confirm password")
    )

    class Meta:
        model  = Institution
        fields = ['name', 'cnpj', 'email', 'cep', 'state', 'city', 'neighborhood', 'street', 'more', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError(_('This email is already in use.'), code='invalid')
        return email

    def clean(self):
        cleaned_data     = super().clean()
        password         = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        validate_password_strength(password)

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', _('Passwords must match.'))
            
        
        return cleaned_data
