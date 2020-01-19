import re

from django.http import HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import login
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.utils import timezone

from musicavis.settings import LOGIN_REDIRECT_URL
from .forms import LoginForm, SignupForm
from app.backend.main.views import index_view


@csrf_protect
@never_cache
def login_view(request, redirect_field_name=REDIRECT_FIELD_NAME, login_form=LoginForm):
    if not isinstance(request.user, AnonymousUser):
        return HttpResponseRedirect(reverse('app:main.index'))

    if request.method == 'POST':
        redirect_to = request.POST.get(redirect_field_name, '')
        form = login_form(data=request.POST)
        if form.is_valid():
            if not redirect_to or ' ' in redirect_to:
                redirect_to = LOGIN_REDIRECT_URL
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                redirect_to = LOGIN_REDIRECT_URL

            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)

            login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        redirect_to = request.GET.get(redirect_field_name, '')
        form = LoginForm(request)

    request.session.set_test_cookie()
    current_site = get_current_site(request)

    args = {
        'title': 'Sign In',
        'hide_nav': True,
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name
    }
    return render(request, 'auth/login.html', args)


@csrf_protect
@never_cache
def signup_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('app:main.index'))

    form = SignupForm()
    if request.method == 'POST':
        data = request.POST.copy()
        data['date_joined'] = timezone.now()
        data['password'] = data['password1']

        form = SignupForm(data=data)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            login(request, user)
            return index_view(request)

    args = {'title': 'Sign Up', 'hide_nav': True, 'form': form}
    return render(request, 'auth/signup.html', args)
