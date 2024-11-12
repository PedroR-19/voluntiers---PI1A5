from django import forms
from positions.models import Position, Category


class MatchForm(forms.Form):
    EMPTY_CHOICE = [('', '---------')]  # Define uma opção vazia
    
    shift = forms.ChoiceField(
        choices=EMPTY_CHOICE + Position.SHIFT_CHOICES,
        required=False
    )

    
    category = forms.ModelChoiceField(
            queryset=Category.objects.all(),
            required=False,
            empty_label='Select Category'
    )

    state = forms.ChoiceField(
        choices=[('', '---')] + [(state, state) for state in Position.objects.values_list('state', flat=True).distinct()],
        required=False
    )
    city = forms.ChoiceField(
        choices=[('', '---')] + [(city, city) for city in Position.objects.values_list('city', flat=True).distinct()],
        required=False
    )
    neighborhood = forms.ChoiceField(
        choices=[('', '---')] + [(neighborhood, neighborhood) for neighborhood in Position.objects.values_list('neighborhood', flat=True).distinct()],
        required=False
    )
