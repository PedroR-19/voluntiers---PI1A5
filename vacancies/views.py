from django.db.models import Q
from django.http.response import Http404
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from vacancies.models import Vacancy, Application
from vacancies.forms import ApplicationForm
from profiles.models import User, Institution, Voluntier
from vacancies.models import Vacancy
from .pagination import make_pagination
from django.utils import translation
from django.utils.translation import gettext as _

PER_PAGE = 6


class VacancyListViewBase(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    ordering = ['-id']
    template_name = 'vacancies/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('vacancies'),
            PER_PAGE
        )

        html_language = translation.get_language()

        ctx.update(
            {'vacancies': page_obj,
             'pagination_range': pagination_range,
             'html_language': html_language,
            }
        )
        return ctx


def vacancy_list_view_home(request):
    user = request.user
    vacancies = Vacancy.objects.all()

    institution = None
    voluntier = None

    if user.is_authenticated and not user.is_superuser:
        try:
            institution = Institution.objects.get(user=user)
        except Institution.DoesNotExist:
            institution = None

        try:
            voluntier = Voluntier.objects.get(user=user)
        except Voluntier.DoesNotExist:
            voluntier = None

    return render(
        request,
        'vacancies/pages/home.html',
        context={
            'user': user,
            'institution': institution,
            'voluntier': voluntier,
            'vacancies': vacancies,
        }
    )


class VacancyListViewCategory(VacancyListViewBase):
    template_name = 'vacancies/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        category_translation = _('Category')

        ctx.update({
            'title': f'{ctx.get("vacancies")[0].category.name} - {category_translation} | '
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs


class VacancyListViewSearch(VacancyListViewBase):
    template_name = 'vacancies/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx


class VacancyDetail(DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'vacancies/pages/vacancy-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        user_profile = None
        if self.request.user.is_authenticated:
            try:
                user_profile = self.request.user.voluntier
            except Voluntier.DoesNotExist:
                user_profile = None

        ctx.update({
            'is_detail_page': True,
            'user_profile': user_profile
        })

        return ctx


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from vacancies.models import Vacancy
from vacancies.forms import ApplicationForm

@login_required
def candidatar_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.vacancy = vacancy
            application.voluntier = request.user.voluntier  # Certifique-se de que estamos associando corretamente
            application.save()
            messages.success(request, 'Sua application foi enviada!')
            return redirect('profiles:dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'vacancies/pages/candidatar_vacancy.html', {'form': form, 'vacancy': vacancy})
