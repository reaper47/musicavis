from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField()
    email_address = forms.EmailField(required=False)
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 8, 'placeholder': "What's on your mind?"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'input'})
        self.fields['email_address'].widget.attrs.update({'class': 'input'})
        self.fields['subject'].widget.attrs.update({'class': 'input'})
        self.fields['message'].widget.attrs.update({'class': 'textarea'})
