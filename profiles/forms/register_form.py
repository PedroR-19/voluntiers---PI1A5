from django                     import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms  import UserCreationForm
from django.core.exceptions     import ValidationError
from .django_forms              import add_placeholder, strong_password
from django.utils.translation   import gettext_lazy as _

from profiles.models import User, Institution, Voluntier


class RegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=[('ONG', 'ONG'), ('Voluntier', 'Voluntier')],
        error_messages={'required': _('Please select an option')},
        label=_('User type')
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        if User.objects.filter(email=email).exists():
            raise ValidationError(_('This email is already in use.'), code='invalid')
        return email


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'cnpj', 'cep', 'state', 'city', 'neighborhood', 'street', 'more']


class VoluntierForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Voluntier
        fields = ['first_name', 'last_name', 'birth_date', 'cpf', 'about', 'linkedin']
