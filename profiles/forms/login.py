from django        import forms
from .django_forms import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['email'], 'Digite seu email')
        add_placeholder(self.fields['password'], 'Digite sua senha')

    email      = forms.EmailField()
    password   = forms.CharField(
        widget = forms.PasswordInput()
    )
