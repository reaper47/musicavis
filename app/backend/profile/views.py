from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from app.models.practice import Instrument
from app.backend.utils.enums import FormType
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
    if current_user.get_task_in_progress('export_practices'):
        flash('An export task is currently in progress')
        return 'task in progress'
    else:
        os = NewLine.from_string(request.user_agent.platform)
        file_type = FileType.from_string(request.form.get('file_type'))
        current_user.launch_task('export_practices', 'Exporting practices...', os=os, file_type=filetype)
        db.session.commit()
    return ''


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
            if change_password_form.is_valid():
                if is_password_correct:
                    user.profile.update_password(data['new_password'])
                    messages.info(request, 'Your password has been updated.')
                    return redirect(reverse('app:profile.settings'))
                messages.info(request, 'Password is incorrect.')
        except KeyError:
            pass

        change_email_form = ChangeEmailForm(user=user, data=data)
        if change_email_form.is_valid():
            if is_password_correct:
                update_email(user, data['new_email'])
                messages.info(request, 'Your email has been updated. A confirmation link has been sent to you.')
                return redirect(reverse('app:profile.settings'))
            messages.info(request, 'Email is invalid.')

        change_username_form = ChangeUsernameForm(data=data)
        if change_username_form.is_valid():
            if is_password_correct:
                user.profile.update_username(data['new_username'])
                messages.info(request, 'Your username has been updated.')
                return redirect(reverse('app:profile.settings'))
            messages.info(request, 'Username is invalid.')

    change_password_form = ChangePasswordForm(user=user)
    change_email_form = ChangeEmailForm(user=user)
    change_username_form = ChangeUsernameForm()
    return _render_access(request, change_password_form, change_email_form, change_username_form)


def _render_access(request, password_form, email_form, username_form):
    form_name = request.POST.get('name', '')
    form_type = FormType.get_form_type([form_name])

    if form_type == FormType.CHANGE_EMAIL:
        password_form.confirm.errors = []
        password_form.new_password.errors = []
        password_form.old_password.errors = []
        username_form.new_username.errors = []
        username_form.password.errors = []
    elif form_type == FormType.CHANGE_PASSWORD:
        username_form.new_username.errors = []
        username_form.password.errors = []
        email_form.confirm.errors = []
        email_form.new_email.errors = []
        email_form.password.errors = []
    elif form_type == FormType.CHANGE_USERNAME:
        password_form.confirm.errors = []
        password_form.new_password.errors = []
        password_form.old_password.errors = []
        email_form.confirm.errors = []
        email_form.new_email.errors = []
        email_form.password.errors = []

    args = dict(title='Access Settings',
                password_form=password_form,
                email_form=email_form,
                username_form=username_form,
                username=request.user.username,
                url_delete_account=reverse('app:profile.delete_account'))

    return render(request, 'profile/settings_access.html', args)


@login_required
def settings_practice_view(request):
    if request.method == 'POST':
        data = request.POST.copy()

        form = SelectDefaultInstrumentForm(data=data)
        if form.is_valid():
            instruments = [Instrument.objects.get(name=name.title()) for name in form.cleaned_instruments if name != 'None']
            request.user.profile.update_instruments_practiced(instruments)

            instruments_string = ', '.join([x.name for x in instruments]) if instruments else 'None'
            messages.info(request, f'Your instruments practiced have been set to {instruments_string}.')
            return redirect(reverse('app:profile.settings'))

    args = dict(title='Practice Settings', form=SelectDefaultInstrumentForm())
    return render(request, 'profile/settings_practice.html', args)


@require_POST
@login_required
def add_new_instrument_view(request):
    name = request.args['name'].lower()
    instrument = Instrument.query.filter_by(name=name).first()
    if not name or instrument:
        return '400'

    commit(Instrument(name=name))
    return '200'


@login_required
def settings_profile_view(request):
    form = EmailPreferencesForm(request.user.profile)
    if request.method == 'POST':
        data = request.POST.copy()
        form = EmailPreferencesForm(data=data)
        if form.is_valid():
            request.user.profile.update_email_preferences(data['features'], data['practicing'], data['promotions'])
            return redirect(reverse('app:profile.settings'))

    args = dict(title='Profile Settings', form=form)
    return render(request, 'profile/settings_profile.html', args)


@require_POST
def delete_account_view(request):
    args = request.get_json()
    if current_user.is_anonymous or not current_user.verify_password(args['password']):
        return url_for('main.index'), 400

    username = current_user.username.title()
    logout_user()
    delete_user(username)
    flash(f'Farewell, {username}. We are sad to see you go :(')
    return url_for('main.index')
