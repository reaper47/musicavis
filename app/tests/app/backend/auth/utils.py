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


def reset_post(client, email):
    url = reverse('app:auth.request_password_reset')
    data = dict(email=email)
    return client.post(url, data=data, follow=True)


def reset_password_post(client, token, password1, password2, is_follow=True):
    url = reverse('app:auth.password_reset', args=[token])
    data = dict(password1=password1, password2=password2)
    return client.post(url, data, follow=is_follow)
