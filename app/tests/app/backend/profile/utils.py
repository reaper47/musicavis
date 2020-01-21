from django.urls import reverse

ACCESS_SETTINGS = reverse('app:profile.settings_access')


def change_password(client, old_password, new_password, repeat_new_password):
    data = dict(current_password=old_password,
                new_password=new_password,
                repeat_new_password=repeat_new_password)
    return client.post(ACCESS_SETTINGS, data=data)


def change_email(client, new_email, repeat_email, password):
    data = dict(new_email=new_email,
                repeat_email=repeat_email,
                current_password=password)
    return client.post(ACCESS_SETTINGS, data=data)


def change_username(client, new_username, password):
    data = dict(new_username=new_username,
                current_password=password)
    return client.post(ACCESS_SETTINGS, data=data)
