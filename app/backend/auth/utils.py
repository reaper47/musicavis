from django.urls import reverse

from musicavis.settings import BASE_URL, MUSICAVIS_ADMIN
from app.backend.utils.tasks import send_email
from app.backend.utils.enums import TokenType


def send_email_to_user(user, token_type: TokenType, resend=False):
    username = user.username
    email = user.email

    token = user.profile.generate_token(token_type)
    if token_type == TokenType.CONFIRM:
        template = "confirm" if not resend else "confirm_new"
        __send_confirmation_email(username, email, token, template)
    elif token_type == TokenType.RESET:
        __send_reset_password_request_email(username, email, token)
    elif token_type.UNSUBSCRIBE:
        __send_account_confirmed_email(username, email, token)
    else:
        raise NotImplementedError(f"Send email for {token_type} is not implemented.")


def __send_confirmation_email(username, email, token, template):
    args = dict(
        username=username,
        confirm_url=BASE_URL + reverse("app:auth.confirm", args=[token]),
        resend_url=BASE_URL + reverse("app:auth.resend_confirm", args=[token]),
    )
    send_email.delay([email], "Confirm Your Account", f"auth/email/{template}", args)


def __send_reset_password_request_email(username, email, token):
    args = dict(
        username=username,
        password_reset_url=BASE_URL + reverse("app:auth.password_reset", args=[token]),
    )
    send_email.delay([email], "Reset Your Password", "auth/email/reset_password", args)


def __send_account_confirmed_email(username, email, token):
    args = dict(
        username=username,
        add_unsubscribe=True,
        contact_url=BASE_URL + reverse("app:contact.contact_us"),
        privacy_url=BASE_URL + reverse("app:legal.privacy"),
        terms_url=BASE_URL + reverse("app:legal.terms"),
        unsubscribe_url=BASE_URL + reverse("app:auth.unsubscribe", args=[token]),
        profile_settings_url=BASE_URL + reverse("app:profile.settings"),
        admin=MUSICAVIS_ADMIN,
    )
    send_email.delay([email], "Welcome to Musicavis", "auth/email/welcome", args)


def notLoggedIn(user):
    return not user.is_authenticated
