from django                   import forms
from django.core.exceptions   import ValidationError
from .django_forms            import add_attr
from django.utils.translation import gettext_lazy as _

from collections      import defaultdict
from positions.models import Position, Subcategory


class ProfilepositionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('state'), 'id', 'id_state')
        add_attr(self.fields.get('city'), 'id', 'id_city')
        add_attr(self.fields.get('category'), 'id', 'id_category')
        add_attr(self.fields.get('subcategory'), 'id', 'id_subcategory')


    class Meta:
        model = Position

        fields = [
            'title', 'description', 'category', 'subcategory', 'shift',
            'state', 'city', 'zone','logradouro',
        ]

        widgets = {
            'shift': forms.Select(choices=Position.SHIFT_CHOICES),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cd          = self.cleaned_data

        title       = cd.get('title')
        description = cd.get('description')

        if title == description:
            self._my_errors['title'].append('O Título NÃO pode ser igual à Descrição')
            self._my_errors['description'].append('A Descrição NÃO pode ser igual ao Título')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('Deve ter pelo menos 5 caracteres')

        return title