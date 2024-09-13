from django                   import forms
from django.utils.translation import gettext_lazy as _

from profiles.models import Institution


class InstitutionForm(forms.ModelForm):
    email            = forms.EmailField()
    password         = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label=_("Confirm password"))

    class Meta:
        model  = Institution
        fields = ['name', 'cnpj', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data     = super().clean()
        password         = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords must match.')

        return cleaned_data
