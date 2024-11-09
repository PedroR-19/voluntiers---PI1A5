from django import forms
from profiles.models import Voluntier

class Update_s(forms.ModelForm):
    class Meta:
        model = Voluntier
        fields = ['about', 'linkedin']  