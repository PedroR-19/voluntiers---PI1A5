from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .django_forms import add_placeholder, strong_password
from django.utils.translation import gettext_lazy as _

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['user_type'], 'ONG or Voluntier')
        add_placeholder(self.fields['username'], _('Your name'))
        add_placeholder(self.fields['email'], _('Your e-mail'))
        add_placeholder(self.fields['first_name'], _('Ex.: Pedro'))
        add_placeholder(self.fields['last_name'], _('Ex.: Costa'))
        add_placeholder(self.fields['password'], _('Write your password'))
        add_placeholder(self.fields['password2'], _('Write your password again'))

    user_type = forms.ChoiceField(
        choices=[
            ('ONG', 'ONG'),
            ('Voluntier', 'Voluntier'),
        ],
        error_messages={'required': _('Please select an option')},
        label=_('User_type')
    )
    username = forms.CharField(
        label=_('Username'),
        help_text=_(
            _('Username must contain letters, numbers, or one of these: @.+-_. Username must contain between 4 and 150 characters.')
        ),
        error_messages={
            'required': _('This field must not be empty'),
            'min_length': _('Username must have at least 4 characters'),
            'max_length': _('Username must have less than 150 characters'),
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        error_messages={'required': _('Write your first name')},
        label=_('First name')
    )
    last_name = forms.CharField(
        error_messages={'required': _('Write your last name')},
        label=_('Last name')
    )
    email = forms.EmailField(
        error_messages={'required': _('E-mail is required')},
        label='E-mail',
        help_text=_('The e-mail need to be valid.'),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': _('Password must not be empty')
        },
        help_text=_(
            _('Password must contain at least one uppercase letter, '
            'a lowercase letter and a number. '
            'at least 8 characters.')
        ),
        validators=[strong_password],
        label=_('Password')
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label=_('Password2'),
        error_messages={
            'required': _('Please, repeat your password')
        },
    )

    class Meta:
        model = User
        fields = [
            'user_type',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                _('This email is already in use.'), code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                _('Password and Password2 must be the same'),
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
