from django.db.models import Q
from django.http.response import Http404
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.utils.translation import gettext as _
from django.contrib import messages
from django.utils.decorators import method_decorator
from positions.models import Position, Application
from profiles.models import User, Institution, Voluntier
from .pagination import make_pagination

PER_PAGE = 6

class positionListViewBase(ListView):
    model = Position
    context_object_name = 'positions'
    ordering = ['-id']
    template_name = 'positions/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('positions'),
            PER_PAGE
        )

        html_language = translation.get_language()

        ctx.update({
            'positions': page_obj,
            'pagination_range': pagination_range,
            'html_language': html_language,
        })
        return ctx

def position_list_view_home(request):
    user = request.user
    positions = Position.objects.all()

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
        'positions/pages/home.html',
        context={
            'user': user,
            'institution': institution,
            'voluntier': voluntier,
            'positions': positions,
        }
    )

class positionListViewCategory(positionListViewBase):
    template_name = 'positions/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        category_translation = _('Category')

        ctx.update({
            'title': f'{ctx.get("positions")[0].category.name} - {category_translation} | '
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

class positionListViewSearch(positionListViewBase):
    template_name = 'positions/pages/search.html'

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

@method_decorator(login_required, name='dispatch')
class positionDetail(DetailView):
    model = Position
    context_object_name = 'position'
    template_name = 'positions/pages/position-view.html'

    def post(self, request, *args, **kwargs):
        # Get the position object
        self.object = self.get_object()
        
        # Check if the user is a Voluntier
        try:
            voluntier = request.user.voluntier
        except Voluntier.DoesNotExist:
            voluntier = None

        if voluntier:
            # Create an Application object
            Application.objects.create(
                position=self.object,
                voluntier=voluntier
            )
            messages.success(request, _('Your application has been submitted successfully'))
            return redirect('profiles:dashboard')  # Redirect to the dashboard or another appropriate page

        messages.error(request, 'You need to be a Voluntier to apply.')
        return redirect('positions:position', pk=self.object.pk)

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
    
class positionListViewInstitution(positionListViewBase):
    template_name = 'positions/pages/institution.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        institution_translation = _('Institution')
        
        # Get the institution name for the title
        institution = get_object_or_404(Institution, id=self.kwargs.get('institution_id'))
        
        ctx.update({
            'title': f'{institution.name} - {institution_translation} | '
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            profile__id=self.kwargs.get('institution_id')
        )

        if not qs:
            raise Http404()

        return qs
