from django.contrib.auth.models import User

from app.models.practice import Practice, Instrument
from app.models.task import Task

A_USERNAME = 'test'
OTHER_USERNAME = 'PuertoRico'
AN_EMAIL = 'test@test.ssh'
OTHER_EMAIL = 'puertorico@test.ssh'
A_PASSWORD = 'helloworld!'
OTHER_PASSWORD = 'goodbyeworld!'
SOME_INSTRUMENTS = ['Violin', 'Drums']
AN_INSTRUMENT = 'Piano'


"""
PROFILE
"""


def delete_users():
    User.objects.all().delete()


def create_user(username=A_USERNAME, email=AN_EMAIL, password=A_PASSWORD):
    return User.objects.create_user(username, email, password)


def create_user_with_a_practice():
    user = User.objects.create_user(OTHER_USERNAME, OTHER_EMAIL, OTHER_PASSWORD)
    practice = create_practice(user=user)
    user.profile.practices.add(practice)
    return user


"""
PRACTICE
"""


def create_practice(user=None) -> Practice:
    user = user if user else create_user(A_USERNAME, AN_EMAIL, A_PASSWORD)
    instrument = create_instrument(AN_INSTRUMENT)
    practice = Practice(user_profile=user.profile, instrument=instrument)
    practice.save()
    return practice


def create_complete_practice(user, instrument, date, exercises=None, goals=None,
                             improvements=None, positives=None, notes=''):
    instrument.save()

    practice = Practice(user_profile=user.profile, date=date, instrument=instrument, notes=notes)
    practice.save()

    if exercises:
        for exercise in exercises:
            exercise.save()
            practice.exercises.add(exercise)

    if goals:
        for goal in goals:
            goal.save()
            practice.goals.add(goal)

    if improvements:
        for improvement in improvements:
            improvement.save()
            practice.improvements.add(improvement)

    if positives:
        for positive in positives:
            positive.save()
            practice.positives.add(positive)

    return practice


def create_instrument(name: str) -> Instrument:
    instrument = Instrument.objects.filter(name=name).first()
    if not instrument:
        instrument = Instrument(name=name)
        instrument.save()
    return instrument


def add_instruments_to_database():
    for name in SOME_INSTRUMENTS:
        instrument = Instrument(name=name)
        instrument.save()


"""
TASKS
"""


class JobMock:

    def __init__(self):
        self.id = 1

    def get_id(self):
        return self.id


def create_task(id, name, description, profile, complete=False):
    task = Task(id=id, name=name, description=description, user_profile=profile, complete=complete)
    task.save()
    return task


"""
VIEWS
"""


def is_user_index(response):
    components = ['New Practice Session', 'Past Practice Sessions']
    return all_equal(response, components)


def is_anonymous_index(response):
    components = ['Musicavis']
    return all_equal(response, components)


def is_login_form(response):
    components = ['Username', 'Password', 'Remember Me', 'Log In', 'Forgot Password?', 'Create an Account']
    return all_equal(response, components)


def is_signup_form(response):
    components = ['Username', 'Email', 'Password', 'Password confirmation', 'Sign Up',
                  'emails', 'Terms of Use', 'Privacy Policy']
    return all_equal(response, components)


def is_password_reset_form(response):
    components = ['Email', 'Reset Password', 'Password Reset Request']
    return all_equal(response, components)


def is_reset_password_form(response):
    components = ['Reset Your Password', 'New Password', 'Confirm Password']
    return all_equal(response, components)


def is_contact_form(response, is_user_logged_in=True):
    components = ['First name', 'Subject:', 'Message:', 'Send']
    componentsNotLoggedIn = ['Email address']
    has_components = all_equal(response, components)
    has_other_components = all_equal(response, componentsNotLoggedIn)

    if is_user_logged_in:
        return has_components and has_other_components
    return has_components and not has_other_components


def is_profile_page(response):
    components = ['Instruments Practiced', 'Settings', 'Export Practices']
    return all_equal(response, components) and b'gravatar.com' in response.content


def is_settings_page(response):
    components = ['Access', 'Change email', 'Change password', 'Change username',
                  'Practice', 'instruments practiced', 'Profile', 'Email preferences']
    return all_equal(response, components)


def is_access_settings(response):
    components = ['Current password', 'New password', 'Repeat new password',
                  'New email', 'Repeat email', 'Password', 'New username']
    return all_equal(response, components)


def is_practice_settings_page(response):
    components = ['instruments you practice', 'not listed', 'Save']
    return all_equal(response, components)


def is_profile_settings_page(response):
    components = ['Email preferences', 'Agree to receive', 'Practicing', 'Promotions', 'Features']
    return all_equal(response, components)


def all_equal(response, components):
    return all(c.encode() in response.content for c in components)
