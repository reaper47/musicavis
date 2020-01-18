from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 8, 'placeholder': "What's on your mind?"}))

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()

        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')

        if not name and not email and not message:
            raise forms.ValidationError('Your message to us cannot be empty')
