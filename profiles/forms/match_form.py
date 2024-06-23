# profiles/forms/match_form.py
from django import forms
from vacancies.models import Vacancy, Category

class MatchForm(forms.Form):
    shift = forms.ChoiceField(choices=Vacancy.SHIFT_CHOICES, required=False)
    country = forms.ChoiceField(choices=Vacancy.COUNTRY_CHOICES, required=False)
    state = forms.ChoiceField(choices=Vacancy.STATE_CHOICES, required=False)
    city = forms.ChoiceField(choices=Vacancy.CITY_CHOICES, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
