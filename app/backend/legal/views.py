from django.shortcuts import render


def privacy_view(request):
    args = {'title': 'Privacy Policy'}
    return render(request, 'privacy.html', args)


def terms_view(request):
    args = {'title': 'Terms of Use'}
    return render(request, 'terms.html', args)
