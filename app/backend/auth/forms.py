from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(label='Remember Me', initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input', 'autofocus': 'autofocus'})
        self.fields['password'].widget.attrs.update({'class': 'input'})
        self.fields['remember_me'].widget.attrs.update({'class': 'checkbox big-input-checkbox'})


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = '__all__'

    email = forms.EmailField()

    text = 'I agree to receive instructional and promotional emails'
    send_emails = forms.BooleanField(label=text, initial=False, required=False)

    text = mark_safe('I agree to the <a href="/terms">Terms of Use</a> & <a href="/privacy">Privacy Policy</a>')
    agree_terms = forms.BooleanField(label=text, initial=False)

    password = forms.CharField(widget=forms.HiddenInput(), required=False)
    date_joined = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input', 'autofocus': 'autofocus'})

        for field in ['email', 'password1', 'password2']:
            self.fields[field].widget.attrs.update({'class': 'input'})

        for field in ['send_emails', 'agree_terms']:
            self.fields[field].widget.attrs.update({'class': 'checkbox big-input-checkbox'})

    def clean(self):
        cleaned_data = super().clean()

        for field in ['username', 'email', 'password1', 'password2', 'agree_terms']:
            if not cleaned_data.get(field):
                raise forms.ValidationError('You must fill the fields, and agree to the terms of use.')

        if User.objects.filter(email=cleaned_data.get('email')).first():
            raise forms.ValidationError('Email already registerd.')

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.is_active = True
            user.save()

            if not self.cleaned_data['send_emails']:
                user.profile.email_preferences.features = False
                user.profile.email_preferences.practicing = False
                user.profile.email_preferences.promotions = False
                user.profile.email_preferences.save()

        return user


class ResetPasswordRequestForm(forms.Form):
    email = forms.EmailField(label='Email address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'input', 'autofocus': 'autofocus'})


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'input', 'autofocus': 'autofocus'})
        self.fields['password2'].widget.attrs.update({'class': 'input'})
