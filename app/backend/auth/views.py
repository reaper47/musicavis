import re

from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from musicavis.settings import LOGIN_REDIRECT_URL, BASE_URL
from .forms import LoginForm, SignupForm, ResetPasswordRequestForm, ResetPasswordForm
from app.backend.auth.utils import send_email_to_user, notLoggedIn
from app.models.profile import get_user_from_token, Profile
from app.backend.utils.enums import TokenType


@csrf_protect
@never_cache
def login_view(request, redirect_field_name=REDIRECT_FIELD_NAME, login_form=LoginForm):
    if not request.user.is_anonymous:
        return redirect(reverse('app:main.index'))

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

            return redirect(redirect_to)
    else:
        redirect_to = request.GET.get(redirect_field_name, '')
        form = LoginForm(request)

    request.session.set_test_cookie()
    current_site = get_current_site(request)

    args = dict(title='Sign In', hide_nav=True, form=form, site=current_site, site_name=current_site.name)
    args[redirect_field_name] = redirect_to
    return render(request, 'auth/login.html', args)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect(reverse('app:main.index'))


@csrf_protect
@never_cache
@user_passes_test(notLoggedIn, login_url='/', redirect_field_name=None)
def signup_view(request):
    form = SignupForm()
    if request.method == 'POST':
        data = request.POST.copy()
        data['date_joined'] = timezone.now()
        data['password'] = data['password1']

        form = SignupForm(data=data)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            send_email_to_user(user, TokenType.CONFIRM)
            messages.info(request, 'Sign up complete. An account confirmation has been sent to you by email.')
            return redirect(reverse('app:auth.login'))

    args = {'title': 'Sign Up', 'hide_nav': True, 'form': form}
    return render(request, 'auth/signup.html', args)


def account_confirm(request, token):
    user = get_user_from_token(token, TokenType.CONFIRM)

    if user is None:
        message = 'The confirmation link is invalid or has expired.'
    elif user.profile.is_confirmed:
        message = 'Your account is already confirmed.'
    elif user.profile.confirm(token):
        user.profile.is_confirmed = True
        user.save()
        send_email_to_user(user, TokenType.UNSUBSCRIBE)
        message = f'Thank you {user.username}! Your account has been confirmed.'

    messages.info(request, message)
    return redirect(reverse('app:main.index'))


@csrf_protect
@never_cache
def resend_account_confirm(request, token):
    user = get_user_from_token(token, TokenType.CONFIRM)

    if user is None:
        message = 'The confirmation link is invalid or has expired.'
    elif user.profile.is_confirmed:
        message = 'Your account is already confirmed.'
    else:
        message = 'A new account confirmation has been sent to you by email.'
        send_email_to_user(user, TokenType.CONFIRM, resend=True)

    messages.info(request, message)
    return redirect(reverse('app:main.index'))


@csrf_protect
@never_cache
@user_passes_test(notLoggedIn, login_url='/', redirect_field_name=None)
def request_password_reset_view(request):
    if request.method == 'POST':
        data = request.POST.copy()
        form = ResetPasswordRequestForm(data=data)
        if form.is_valid():
            user = User.objects.filter(email=data['email']).first()
            if user:
                send_email_to_user(user, TokenType.RESET)

            messages.info(request, 'An email with instructions to reset your password has been sent to you')
            return redirect(reverse('app:auth.login'))

    form = ResetPasswordRequestForm()
    args = dict(title='Password Reset Request', hide_nav=True, form=form)
    return render(request, 'auth/reset_password_request.html', args)


@csrf_protect
@never_cache
@user_passes_test(notLoggedIn, login_url='/', redirect_field_name=None)
def password_reset_view(request, token):
    if request.method == 'POST':
        data = request.POST.copy()
        form = ResetPasswordForm(data=data)
        if form.is_valid():
            if Profile.reset_password(token, data['password1']):
                messages.info(request, 'Your password has been updated.')
                return redirect(reverse('app:auth.login'))
            else:
                return redirect(reverse('app:main.index'))

    form = ResetPasswordForm()
    args = dict(title='Reset Your Password', hide_nav=True, form=form)
    return render(request, 'auth/reset_password.html', args)


def unsubscribe_view(request, token):
    user = get_user_from_token(token, TokenType.UNSUBSCRIBE)

    is_unsubscribed = user is not None
    if is_unsubscribed:
        request.user.profile.update_email_preferences(False, False, False)

    args = dict(
        title='Unsubscribe',
        is_unsubscribed=is_unsubscribed,
        contact_url=BASE_URL + reverse('app:contact.contact_us')
    )
    return render(request, 'auth/unsubscribe.html', args)
