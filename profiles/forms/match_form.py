from django import forms
from positions.models import Position, Category


class MatchForm(forms.Form):
    EMPTY_CHOICE = [('', '---------')]  # Define uma opção vazia
    
    shift = forms.ChoiceField(
        choices=EMPTY_CHOICE + Position.SHIFT_CHOICES,
        required=False
    )

    state = forms.ChoiceField(
        choices=EMPTY_CHOICE + Position.STATE_CHOICES,
        required=False
    )

    city = forms.ChoiceField(
        choices=EMPTY_CHOICE + Position.CITY_CHOICES,
        required=False
    )

    zone = forms.ChoiceField(
        choices=EMPTY_CHOICE + Position.ZONE_CHOICES,
        required=False
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='Select Category'
    )
