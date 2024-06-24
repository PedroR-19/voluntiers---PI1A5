from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from profiles.forms.vacancy_form import ProfileVacancyForm
from vacancies.models import Vacancy
from profiles.models import Institution

@method_decorator(
    login_required(login_url='profiles:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardVacancy(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        return super().setup(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_vacancy(self, id=None):
        vacancy = None

        if id is not None:
            vacancy = Vacancy.objects.filter(
                profile__user=self.request.user,  # Ajuste para garantir que estamos filtrando pelo usuário da instituição
                pk=id,
            ).first()

            if not vacancy:
                raise Http404()

        return vacancy

    def render_vacancy(self, form):
        return render(
            self.request,
            'profiles/pages/dashboard_vacancy.html',
            context={
                'form': form
            }
        )

    def get(self, request, id=None):
        vacancy = self.get_vacancy(id)
        form = ProfileVacancyForm(instance=vacancy)
        return self.render_vacancy(form)

    def post(self, request, id=None):
        vacancy = self.get_vacancy(id)
        form = ProfileVacancyForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=vacancy
        )

        if form.is_valid():
            vacancy = form.save(commit=False)

            institution = get_object_or_404(Institution, user=request.user)  # Obtenha a instituição do usuário
            vacancy.profile = institution  # Associe a vaga à instituição
            vacancy.requirements_is_html = False

            vacancy.save()

            messages.success(request, 'Sua vaga foi salva com sucesso!')
            return redirect(
                reverse(
                    'profiles:dashboard_vacancy_edit', args=(
                        vacancy.id,
                    )
                )
            )

        return self.render_vacancy(form)


@method_decorator(
    login_required(login_url='profiles:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardVacancyDelete(DashboardVacancy):
    def post(self, *args, **kwargs):
        vacancy = self.get_vacancy(self.request.POST.get('id'))
        vacancy.delete()
        messages.success(self.request, 'Deleted successfully.')
        return redirect(reverse('profiles:dashboard'))
