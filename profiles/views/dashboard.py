# profiles/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from vacancies.models import Vacancy, Application
from profiles.models import User, Institution, Voluntier

@login_required
def dashboard(request):
    profile = request.user.profile

    # Inicializa o contexto com o perfil e o tipo de usuário
    context = {
        'profile': profile,
        'user_type': profile.user_type,
    }

    # Identifica o tipo de usuário e busca os dados correspondentes
    if profile.user_type == 'Voluntier':
        applications = Application.objects.filter(voluntier=request.user)
        context['applications'] = applications
    else:
        vacancies = Vacancy.objects.filter(profile=request.user)
        context['vacancies'] = vacancies

    return render(request, 'profiles/pages/dashboard.html', context)
