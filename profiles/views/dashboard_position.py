from django.contrib                 import messages
from django.contrib.auth.decorators import login_required
from django.http.response           import Http404
from django.shortcuts               import redirect, render, get_object_or_404
from django.urls                    import reverse
from django.utils.decorators        import method_decorator
from django.views                   import View

from profiles.forms.position_form import ProfilepositionForm
from positions.models             import Position
from profiles.models              import Institution


@method_decorator(
    login_required(login_url='profiles:login', redirect_field_name='next'),
    name='dispatch'
)


class Dashboardposition(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        return super().setup(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_position(self, id=None):
        position = None

        if id is not None:
            position = Position.objects.filter(
                profile__user=self.request.user,  # Ajuste para garantir que estamos filtrando pelo usuário da instituição
                pk=id,
            ).first()

            if not position:
                raise Http404()

        return position

    def render_position(self, form):
        return render(
            self.request,
            'profiles/pages/dashboard_position.html',
            context={
                'form': form
            }
        )

    def get(self, request, id=None):
        position = self.get_position(id)
        form = ProfilepositionForm(instance=position)
        return self.render_position(form)

    def post(self, request, id=None):
        position = self.get_position(id)
        form = ProfilepositionForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=position
        )

        if form.is_valid():
            position = form.save(commit=False)

            institution = get_object_or_404(Institution, user=request.user)  # Obtenha a instituição do usuário
            position.profile = institution  # Associe a vaga à instituição

            position.save()

            messages.success(request, 'Sua vaga foi criada com sucesso')
            return redirect(
                reverse(
                    'profiles:dashboard_position_edit', args=(
                        position.id,
                    )
                )
            )

        return self.render_position(form)


@method_decorator(
    login_required(login_url='profiles:login', redirect_field_name='next'),
    name='dispatch'
)


class DashboardpositionDelete(Dashboardposition):
    def post(self, *args, **kwargs):
        position = self.get_position(self.request.POST.get('id'))
        position.delete()
        messages.success(self.request, 'Vaga deletada com sucesso')
        return redirect(reverse('profiles:dashboard'))