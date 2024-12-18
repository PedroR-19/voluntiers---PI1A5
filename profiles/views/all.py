from django.contrib                 import messages
from django.contrib.auth            import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http                    import Http404
from django.shortcuts               import redirect, render, get_object_or_404
from django.urls                    import reverse
from django.utils.translation       import gettext as _
from django import forms
from profiles.forms.match_form import MatchForm
from profiles.forms            import LoginForm, InstitutionForm, VoluntierForm
from profiles.models           import User, Institution, Voluntier
from positions.models          import Position, Application
from profiles.payments import create_payment_preference



class Update_Voluntier_Form(forms.ModelForm):
    class Meta:
        model = Voluntier
        fields = ['about', 'linkedin']  

def register_choice_view(request):
    return render(request, 'profiles/pages/register_choice.html')


def institution_register_view(request):
    if request.method == 'POST':
        form = InstitutionForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            Institution.objects.create(user=user, name=form.cleaned_data['name'], cnpj=form.cleaned_data['cnpj'],
                                       cep=form.cleaned_data['cep'], state=form.cleaned_data['state'], 
                                       city=form.cleaned_data['city'], neighborhood=form.cleaned_data['neighborhood'],
                                       street=form.cleaned_data['street'], more=form.cleaned_data['more'],)
            messages.success(request, _('Your Institution has been created, please log in.'))
            return redirect(reverse('profiles:login'))
    else:
        form = InstitutionForm()
    return render(request, 'profiles/pages/institution_register.html', {'form': form})


def voluntier_register_view(request):
    if request.method == 'POST':
        form = VoluntierForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            Voluntier.objects.create(user=user, first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], 
                                     birth_date=form.cleaned_data['birth_date'], cpf=form.cleaned_data['cpf'])
            messages.success(request, _('Your Voluntier account has been created, please log in.'))
            return redirect(reverse('profiles:login'))
    else:
        form = VoluntierForm()
    return render(request, 'profiles/pages/voluntier_register.html', {'form': form})


def login_view(request):
    form = LoginForm()
    return render(request, 'profiles/pages/login.html', {
        'form': form,
        'form_action': reverse('profiles:login_create')
    })


def match_view(request):
    form = MatchForm(request.GET or None)
    positions = Position.objects.all()

    if form.is_valid():
        if form.cleaned_data['shift']:
            positions = positions.filter(shift=form.cleaned_data['shift'])

        if form.cleaned_data['state']:
            positions = positions.filter(state__iexact=form.cleaned_data['state'])

        if form.cleaned_data['city']:
            positions = positions.filter(city__iexact=form.cleaned_data['city'])

        if form.cleaned_data['neighborhood']:
            positions = positions.filter(neighborhood__iexact=form.cleaned_data['neighborhood'])

        if form.cleaned_data['category']:
            positions = positions.filter(category=form.cleaned_data['category'])

    return render(request, 'positions/pages/match.html', {
        'positions': positions,
        'form': form,
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        email   = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        # Atualize a autenticação para usar o email como username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, _("You're logged in!"))
            return redirect(reverse('profiles:dashboard'))
        else:
            messages.error(request, _('Invalid credentials'))
    else:
        messages.error(request, _('Invalid email or password'))

    return redirect(reverse('profiles:login'))


@login_required(login_url='profiles:login', redirect_field_name='next')
def logout_view(request):
    if request.method != 'POST':
        messages.error(request, _('Invalid logout request'))
        return redirect(reverse('profiles:login'))

    logout(request)
    messages.success(request, _('Logout Done Successfully'))
    return redirect(reverse('profiles:login'))


@login_required(login_url='profiles:login', redirect_field_name='next')
def dashboard(request):
    user = request.user
    match_form = MatchForm(request.GET or None)
    voluntier_form = None  # Initialize as None

    user_type = None
    profile = None

    if not request.user.is_superuser:
        try:
            institution = Institution.objects.get(user=user)
            user_type = 'ONG'
            profile = institution
        except Institution.DoesNotExist:
            institution = None

        try:
            voluntier = Voluntier.objects.get(user=user)
            user_type = 'Voluntier'
            profile = voluntier
            # Initialize the VoluntierForm with existing data
            voluntier_form = Update_Voluntier_Form(request.POST or None, instance=voluntier)

            if request.method == 'POST' and voluntier_form.is_valid():
                voluntier_form.save()
                messages.success(request, _('Voluntier data saved successfully'))
                return redirect('profiles:dashboard')

        except Voluntier.DoesNotExist:
            voluntier = None

        if user_type == 'Voluntier':
            applications = Application.objects.filter(voluntier=profile)
            return render(
                request,
                'profiles/pages/dashboard.html',
                context={
                    'applications': applications,
                    'user_type': user_type,
                    'user': user,
                    'profile': profile,
                    'form': match_form,
                    'voluntier_form': voluntier_form,  # Add the VoluntierForm to the context
                }
            )

        elif user_type == 'ONG':
            positions = Position.objects.filter(profile=institution)
            return render(
                request,
                'profiles/pages/dashboard.html',
                context={
                    'positions': positions,
                    'user_type': user_type,
                    'user': user,
                    'profile': profile,
                    'form': match_form,
                }
            )
    else:
        # Logic for superuser if needed
        pass

    return render(request, 'profiles/pages/dashboard.html', {'form': match_form})


def payment_view(request):
    preference_id = create_payment_preference()
    
    mercado_pago_url = f"https://www.mercadopago.com.br/checkout/v1/redirect?pref_id={preference_id}"
    return redirect(mercado_pago_url)


@login_required
def payment_success(request):
    try:
        institution = request.user.institution
        institution.is_premium = True
        institution.save()
        messages.success(request, _('Your payment was successful, and your account is now premium!'))
    except Institution.DoesNotExist:
        messages.error(request, _('Institution not found.'))
    return redirect('profiles:dashboard')

@login_required
def payment_failure(request):
    messages.error(request, _('There was an issue with your payment. Please try again.'))
    return redirect('profiles:dashboard')

@login_required
def payment_pending(request):
    messages.info(request, _('Your payment is pending. We will notify you once it is complete.'))
    return redirect('profiles:dashboard')