from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[a-z][a-z0-9_]+$"
    message = (
        "Enter a valid username. This value may contain only lowercase ASCII letters, "
        "numbers, and underscores. Must start with a letter."
    )
    flags = 0
