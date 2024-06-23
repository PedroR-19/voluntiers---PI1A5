from collections import defaultdict
from django import forms
from django.core.exceptions import ValidationError
from vacancies.models import Vacancy, Subcategory
from .django_forms import add_attr
from .strings import is_positive_number
from django.utils.translation import gettext_lazy as _


class ProfileVacancyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('requirements'), 'class', 'span-2')

    class Meta:
        model = Vacancy
        fields = [
            'title', 'description', 'category', 'subcategory', 'shift',
            'country', 'state', 'city', 'logradouro', 'requirements', 'cover',
        ]
        widgets = {
            'cover': forms.FileInput(attrs={'class': 'span-2'}),
            'shift': forms.Select(choices=Vacancy.SHIFT_CHOICES),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cd = self.cleaned_data

        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self._my_errors['title'].append('Cannot be equal to description')
            self._my_errors['description'].append('Cannot be equal to title')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('Must have at least 5 chars.')

        return title