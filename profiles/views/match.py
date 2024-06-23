# profiles/views/match.py
from django.shortcuts import render
from vacancies.models import Vacancy
from profiles.forms.match_form import MatchForm

def match_view(request):
    form = MatchForm(request.GET or None)
    vacancies = Vacancy.objects.all()

    if form.is_valid():
        if form.cleaned_data['shift']:
            vacancies = vacancies.filter(shift=form.cleaned_data['shift'])
        if form.cleaned_data['country']:
            vacancies = vacancies.filter(country=form.cleaned_data['country'])
        if form.cleaned_data['state']:
            vacancies = vacancies.filter(state=form.cleaned_data['state'])
        if form.cleaned_data['city']:
            vacancies = vacancies.filter(city=form.cleaned_data['city'])
        if form.cleaned_data['category']:
            vacancies = vacancies.filter(category=form.cleaned_data['category'])

    return render(request, 'vacancies/pages/match.html', {
        'vacancies': vacancies,
        'form': form,
    })
