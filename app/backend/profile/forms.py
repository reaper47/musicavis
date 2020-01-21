from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from app.models.practice import Instrument
from app.backend.utils.enums import FileType

username_validator = RegexValidator(regex='^[A-Za-z][A-Za-z0-9_.]*$',
                                    message='Usernames must have only letters, numbers, dots or underscores',
                                    code='invalid_username')


class SelectFileTypeForm(forms.Form):
    filetype = forms.ChoiceField(label='Select your preferred file format',
                                widget=forms.Select,
                                choices=((x.value, FileType.description(x)) for x in FileType))


class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(validators=[username_validator])
    current_password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_username'].widget.attrs.update({'class': 'input', 'autofocus': 'autofocus'})
        self.fields['current_password'].widget.attrs.update({'class': 'input'})

    def clean_new_username(self):
        username = self.cleaned_data['new_username']
        if User.objects.filter(username=username).first():
            raise forms.ValidationError('Username already taken')


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    repeat_new_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['current_password'].widget.attrs.update({'class': 'input', 'autofocus': 'autofocus'})
        self.fields['new_password'].widget.attrs.update({'class': 'input'})
        self.fields['repeat_new_password'].widget.attrs.update({'class': 'input'})

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data['current_password']
        new_password = cleaned_data['new_password']
        repeat_new_password = cleaned_data['repeat_new_password']

        if not self.user.check_password(current_password):
            raise forms.ValidationError('The current password is incorrect.')

        if new_password != repeat_new_password:
            raise forms.ValidationError('Passwords do not match.')


class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField()
    repeat_email = forms.EmailField()
    current_password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['new_email'].widget.attrs.update({'class': 'input', 'autofocus': 'autofocus'})
        self.fields['repeat_email'].widget.attrs.update({'class': 'input'})
        self.fields['current_password'].widget.attrs.update({'class': 'input'})

    def clean_current_password(self):
        password = self.cleaned_data['current_password']
        if not self.user.check_password(password):
            raise forms.ValidationError('The password is incorrect.')


class SelectDefaultInstrumentForm(forms.Form):
    instruments = forms.MultipleChoiceField(label='Select the instruments you practice',
                                            required=False,
                                            choices=[])
    new_instrument = forms.CharField(label='Add a new instrument', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = sorted([(x.name.lower(), x.name.title()) for x in Instrument.objects.all()])
        choices.insert(0, (str(None), 'None'))
        self.fields['instruments'].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_instruments = cleaned_data['instruments']


class EmailPreferencesForm(forms.Form):
    practicing = forms.BooleanField(label='Anything related to practicing', required=False)
    promotions = forms.BooleanField(label='Promotions and discounts', required=False)
    features = forms.BooleanField(label='Product features', required=False)

    def __init__(self, profile=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['practicing'].widget.attrs.update({'class': 'checkbox big-input-checkbox'})
        self.fields['promotions'].widget.attrs.update({'class': 'checkbox big-input-checkbox'})
        self.fields['features'].widget.attrs.update({'class': 'checkbox big-input-checkbox'})

        if profile:
            self.fields['practicing'].initial = profile.email_preferences.practicing
            self.fields['promotions'].initial = profile.email_preferences.promotions
            self.fields['features'].initial = profile.email_preferences.features
