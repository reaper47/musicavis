from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import ContactForm
from app.backend.utils.tasks import send_email


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            subject = data["subject"]
            email = (
                data["email_address"]
                if request.user.is_anonymous
                else request.user.email
            )
            message = data["message"].splitlines()

            args = dict(message=message, name=data["first_name"], email=email)
            send_email.delay([email], subject, "contact/email/contact_us", args)

            messages.info(
                request,
                "Thank you for contacting us! We will come back to you shortly.",
            )
            return redirect(reverse("app:main.index"))

    form = ContactForm
    args = {"title": "Contact Us", "form": form}
    return render(request, "contact/contact.html", args)
