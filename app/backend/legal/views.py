from django.shortcuts import render


def privacy_view(request):
    args = {"title": "Privacy Policy"}
    return render(request, "legal/privacy.html", args)


def terms_view(request):
    args = {"title": "Terms of Use"}
    return render(request, "legal/terms.html", args)
