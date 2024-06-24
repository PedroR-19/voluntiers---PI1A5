from django import forms
from vacancies.models import Vacancy, Category

class MatchForm(forms.Form):
    EMPTY_CHOICE = [('', '---------')]  # Define uma opção vazia
    
    shift = forms.ChoiceField(
        choices=EMPTY_CHOICE + Vacancy.SHIFT_CHOICES,
        required=False
    )
    country = forms.ChoiceField(
        choices=EMPTY_CHOICE + Vacancy.COUNTRY_CHOICES,
        required=False
    )
    state = forms.ChoiceField(
        choices=EMPTY_CHOICE + Vacancy.STATE_CHOICES,
        required=False
    )
    city = forms.ChoiceField(
        choices=EMPTY_CHOICE + Vacancy.CITY_CHOICES,
        required=False
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='Select Category'
    )
