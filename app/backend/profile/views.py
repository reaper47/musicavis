import json

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse

from app.models.practice import Instrument
from app.backend.utils.enums import NewLine, FileType
from .utils import update_email
from .forms import (SelectFileTypeForm, ChangePasswordForm, ChangeUsernameForm,
                    ChangeEmailForm, EmailPreferencesForm, SelectDefaultInstrumentForm)


@login_required
def profile_view(request):
    args = dict(title='Profile',
                filetype_form=SelectFileTypeForm(),
                instruments_played=request.user.profile.list_instruments_practiced_html(),
                avatar=request.user.profile.avatar(256),
                url_settings=reverse('app:profile.settings'),
                url_export_practices=reverse('app:profile.export_practices'))
    return render(request, 'profile/profile.html', args)


@require_POST
@login_required
def export_practices_view(request):
    if request.user.profile.get_task_in_progress('export_practices'):
        messages.info(request, 'An export task is currently in progress')
        return HttpResponse('task in progress')

    os = NewLine.from_string(request.META['HTTP_USER_AGENT'])
    file_type = FileType.from_string(request.POST['file_type'])
    request.user.profile.launch_task('export_practices', 'Exporting practices...', os=os, file_type=file_type)
    return HttpResponse('')


@login_required
def settings_view(request):
    options = ['Change password', 'Change username', 'Change email', 'Delete account']
    args = dict(options=options,
                url_settings_profile=reverse('app:profile.settings_profile'),
                url_settings_practice=reverse('app:profile.settings_practice'),
                url_settings_access=reverse('app:profile.settings_access'))
    return render(request, 'profile/settings.html', args)


@login_required
def settings_access_view(request):
    user = request.user

    if request.method == 'POST':
        data = request.POST.copy()
        is_password_correct = user.profile.verify_password(data['current_password'])

        change_password_form = ChangePasswordForm(user=user, data=data)
        try:
            if change_password_form.is_valid() and is_password_correct:
                user.profile.update_password(data['new_password'])
                messages.info(request, 'Your password has been updated.')
                return redirect(reverse('app:profile.settings'))
        except KeyError:
            pass

        change_email_form = ChangeEmailForm(user=user, data=data)
        if change_email_form.is_valid() and is_password_correct:
            update_email(user, data['new_email'])
            messages.info(request, 'Your email has been updated. A confirmation link has been sent to you.')
            return redirect(reverse('app:profile.settings'))

        change_username_form = ChangeUsernameForm(data=data)
        if change_username_form.is_valid() and is_password_correct:
            user.profile.update_username(data['new_username'])
            messages.info(request, 'Your username has been updated.')
            return redirect(reverse('app:profile.settings'))

        errors = (list(change_password_form.errors.items()) +
                  list(change_email_form.errors.items()) +
                  list(change_username_form.errors.items()))
        for error in errors:
            message = error[1].data[0].message
            if message != 'This field is required.':
                messages.info(request, message)

    change_password_form = ChangePasswordForm(user=user)
    change_email_form = ChangeEmailForm(user=user)
    change_username_form = ChangeUsernameForm()
    args = dict(title='Access Settings',
                password_form=change_password_form,
                email_form=change_email_form,
                username_form=change_username_form,
                username=request.user.username,
                url_delete_account=reverse('app:profile.delete_account'))

    return render(request, 'profile/settings_access.html', args)


@login_required
def settings_practice_view(request):
    if request.method == 'POST':
        data = request.POST.copy()

        form = SelectDefaultInstrumentForm(data=data)
        if form.is_valid():
            instruments = [Instrument.objects.get(name=name.title())
                           for name in form.cleaned_instruments if name != 'None']
            request.user.profile.update_instruments_practiced(instruments)

            instruments_string = ', '.join([x.name for x in instruments]) if instruments else 'None'
            messages.info(request, f'Your instruments practiced have been set to {instruments_string}.')
            return redirect(reverse('app:profile.settings'))

    args = dict(title='Practice Settings', form=SelectDefaultInstrumentForm())
    return render(request, 'profile/settings_practice.html', args)


@require_POST
@login_required
def add_new_instrument_view(request):
    name = json.loads(request.body.decode('utf-8'))['name']
    instrument = Instrument.objects.filter(name=name).first()
    if not name or instrument:
        return HttpResponse('400')

    instrument = Instrument.objects.create(name=name)
    return HttpResponse('200')


@login_required
def settings_profile_view(request):
    form = EmailPreferencesForm(request.user.profile)
    if request.method == 'POST':
        data = request.POST.copy()
        form = EmailPreferencesForm(data=data)
        if form.is_valid():
            is_features = form.cleaned_data['features']
            is_practicing = form.cleaned_data['practicing']
            is_promotions = form.cleaned_data['promotions']
            request.user.profile.update_email_preferences(is_features, is_practicing, is_promotions)
            messages.info(request, 'Email preferences have been updated.')
            return redirect(reverse('app:profile.settings'))

    args = dict(title='Profile Settings', form=form)
    return render(request, 'profile/settings_profile.html', args)


@require_POST
@login_required
def delete_account_view(request):
    if not request.user.profile.verify_password(request.POST['password']):
        return redirect(reverse('app:main.index'))

    user = request.user
    logout(request)
    user.profile.delete()
    messages.info(request, f'Farewell, {user.username}. We are sad to see you go :(')
    return redirect(reverse('app:main.index'))
