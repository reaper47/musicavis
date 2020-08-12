from app.backend.utils.enums import TokenType

from app.backend.auth.utils import send_email_to_user


def update_email(user, new_email):
    user.email = new_email
    user.profile.is_confirmed = False
    user.save()

    send_email_to_user(user, TokenType.CONFIRM)
