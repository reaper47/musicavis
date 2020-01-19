from django.contrib.auth.models import User

from app.models.practice import Practice, Instrument
from app.models.task import Task

A_USERNAME = 'test'
OTHER_USERNAME = 'PuertoRico'
AN_EMAIL = 'test@gmail.com'
OTHER_EMAIL = 'puertorico@gmail.com'
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


def all_equal(response, components):
    return all(c.encode() in response.content for c in components)
