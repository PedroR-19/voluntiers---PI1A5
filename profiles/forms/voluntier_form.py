from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from profiles.validators import validate_password_strength, validate_email
from profiles.models import Voluntier, User


class VoluntierForm(forms.ModelForm):
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
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label=_("Birth date")
    )

    class Meta:
        model = Voluntier
        fields = ['first_name', 'last_name', 'birth_date', 'cpf', 'email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('This email is already in use.'), code='invalid')
        return email

    def clean(self):
        cleaned_data = super().clean()
        
        password         = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', _('Passwords must match.'))

        return cleaned_data
    
