from django.urls import reverse


def login_post(client, username, password, follow=False):
    url = reverse('app:auth.login')
    credentials = dict(username=username, password=password)
    return client.post(url, credentials, follow=follow)


def register_post(client, username, email, password, repeat, send_emails=True, agree_terms=True, follow=True):
    url = reverse('app:auth.signup')
    data = dict(username=username, email=email, password1=password,
                password2=repeat, send_emails=send_emails, agree_terms=agree_terms)
    return client.post(url, data, follow=follow)
