from django import forms
from profiles.models import Voluntier


class VoluntierForm(forms.ModelForm):
    email            = forms.EmailField()
    password         = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    birth_date       = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

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
