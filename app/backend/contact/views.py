from django.shortcuts import render

from .forms import ContactForm


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = ContactForm

    args = {'title': 'Contact Us', 'form': form}
    return render(request, 'contact/contact.html', args)
