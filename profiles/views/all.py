from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from profiles.forms.match_form import MatchForm
from profiles.forms import LoginForm, RegisterForm
from profiles.models import Profile
from vacancies.models import Vacancy, Application
from profiles.forms.match_form import MatchForm
from django.utils.translation import gettext as _


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'profiles/pages/register_view.html', {
        'form': form,
        'form_action': reverse('profiles:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        profile = Profile.objects.create(user_id=user.id,
                                         user_type=form.cleaned_data['user_type'])
        profile.save()
        messages.success(request, _('Your user has been created, please log in.'))

        del (request.session['register_form_data'])
        return redirect(reverse('profiles:login'))

    return redirect('profiles:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'profiles/pages/login.html', {
        'form': form,
        'form_action': reverse('profiles:login_create')
    })

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


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, _("You're logged in!"))
            login(request, authenticated_user)
        else:
            messages.error(request, _('Invalid credentials'))
    else:
        messages.error(request, _('Invalid username or password'))

    return redirect(reverse('profiles:dashboard'))


@login_required(login_url='profiles:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, _('Invalid logout request'))
        return redirect(reverse('profiles:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, _('Invalid logout user'))
        return redirect(reverse('profiles:login'))

    messages.success(request, _('Logout Done Successfully'))
    logout(request)
    return redirect(reverse('profiles:login'))


@login_required(login_url='profiles:login', redirect_field_name='next')
def dashboard(request):
    user = request.user
    profile = request.user.profile
    if not request.user.is_superuser:
        profile = Profile.objects.get(user_id=request.user.id)
    if profile.user_type == 'Voluntier':
        applications = Application.objects.filter(
            voluntier=request.user
        )
        return render(
            request,
            'profiles/pages/dashboard.html',
            context={
                'applications': applications,
                'user_type': profile.user_type,
                'user': request.user,
                'profile': profile
            }
        )
    else:
        vacancies = Vacancy.objects.filter(
            profile=request.user
        )
        return render(
            request,
            'profiles/pages/dashboard.html',
            context={
                'vacancies': vacancies,
                'user_type': profile.user_type,
                'user': request.user,
                'profile': profile
            }
        )