from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from app.models.user import User
from django.core.validators import RegexValidator
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

    email_preferences = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input', 'autofocus': 'autofocus'})

        for field in ['email', 'password1', 'password2']:
            self.fields[field].widget.attrs.update({'class': 'input'})

        for field in ['send_emails', 'agree_terms']:
            self.fields[field].widget.attrs.update({'class': 'checkbox big-input-checkbox'})

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        agree_terms = cleaned_data.get('agree_terms')

        if not username or not email or not password or not repeat_password or not agree_terms:
            raise forms.ValidationError('You must fill the fields, and agree to the terms of use.')


    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if not self.cleaned_data['send_emails']:
            user.email_preferences.features = False
            user.email_preferences.practicing = False
            user.email_preferences.promotions = False

        if commit:
            user.save()
        return user


class ResetPasswordRequestRequest(forms.Form):
    pass


class ResetPasswordForm(forms.Form):
    pass
