from django import forms
from django.utils.translation import gettext_lazy as _

from profiles.models import Voluntier


class VoluntierForm(forms.ModelForm):
    email            = forms.EmailField()
    password         = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label=_("Confirm password"))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label=_("Birth date"))

    class Meta:
        model = Voluntier
        fields = ['first_name', 'last_name', 'birth_date', 'cpf', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        
        password         = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords must match.')

        return cleaned_data
    
