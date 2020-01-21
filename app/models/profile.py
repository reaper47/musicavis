import json
import math
from hashlib import md5
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.exc import BadSignature

from musicavis.settings import SECRET_KEY
from .practice import Practice, Instrument
from .email_preferences import EmailPreferences
from .notification import Notification
from .task import Task
from ..backend.utils.tasks import export_practices
from ..backend.utils.enums import FileType, NewLine, TokenType
from ..backend.utils.export import ExportPractices
from ..backend.dashboard.stats import PracticeStats
from ..backend.utils.namedtuples import PracticeGraphData


def get_profile_from_user(user: User):
    return Profile.objects.get(user=user)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    practices = models.ManyToManyField('Practice')
    email_preferences = models.ForeignKey('EmailPreferences', on_delete=models.CASCADE)
    notifications = models.ManyToManyField('Notification')
    is_confirmed = models.BooleanField(default=False)
    instruments_practiced = models.ManyToManyField('Instrument')

    def save(self, *args, **kwargs):
        if not hasattr(self, 'email_preferences'):
            self.user.email = self.user.email.lower()

            email_preferences = EmailPreferences.objects.create(features=True, practicing=True, promotions=True)
            self.email_preferences = email_preferences

        return super().save(*args, **kwargs)

    """
    GENERAL
    """

    def verify_password(self, password: str) -> bool:
        return check_password(password, self.user.password)

    def update_password(self, new_password: str):
        self.user.set_password(new_password)
        self.user.save()

    def update_email(self, new_email: str):
        self.user.email = new_email
        self.user.save()

    def update_username(self, new_username: str):
        self.user.username = new_username
        self.user.save()

    def update_email_preferences(self, accept_features: bool, accept_practicing: bool, accept_promotions: bool):
        email_preferences = EmailPreferences.objects.filter(pk=self.email_preferences.pk)
        email_preferences.update(features=accept_features, practicing=accept_practicing, promotions=accept_promotions)

    def update_instruments_practiced(self, instruments):
        for instrument in self.instruments_practiced.all():
            self.instruments_practiced.remove(instrument)

        for instrument in instruments:
            self.instruments_practiced.add(instrument)

        self.save()

    def avatar(self, size):
        digest = md5(self.user.email.encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def add_notification(self, name, data):
        self.notifications.all().filter(name=name).delete()
        notification = Notification.objects.create(name=name, payload_json=json.dumps(data), user_profile=self)
        self.notifications.add(notification)
        return notification

    def list_instruments_practiced_html(self) -> str:
        instruments = self.instruments_practiced.all()
        html = '<br>- '.join([x.name.title() for x in instruments])
        html = f'- {html}' if instruments else 'None'
        return html

    def delete(self):
        self.email_preferences.delete()
        self.user.delete()
        super().delete()

    def __str__(self):
        return self.user.username

    """
    PRACTICE
    """

    def new_practice(self, instrument_name: str) -> Practice:
        instrument = Instrument.objects.filter(name=instrument_name).first()
        if instrument is None:
            instrument = Instrument.objects.create(name=instrument_name)

        practice = Practice.objects.create(user_profile=self, instrument=instrument)
        self.practices.add(practice)
        return practice

    def delete_practice(self, practice: Practice):
        if practice.user_profile == self:
            practice.delete()

    def export_practices(self, os: NewLine, filetype: FileType):
        export_practices = ExportPractices(self.user.username, self.practices.all(), os)
        return export_practices.export(filetype)

    def get_practice_stats(self):
        return PracticeStats(self.practices.all()) if self.practices.all() else None

    def practice_graph_data(self):
        practices = self.practices.all()
        if not practices:
            return PracticeGraphData([], [])

        data = {x.instrument.name: [] for x in practices}
        for practice in practices:
            date = f'{practice.date:%Y%m%d}'
            data[practice.instrument.name].append({'length': practice.length, 'date': date})

        start_date = min([x.date for x in practices])
        delta = timezone.now() - start_date
        delta_days = math.ceil(delta.days + delta.seconds / 86400)
        dates = [f'{start_date + timedelta(days=i):%Y%m%d}' for i in range(delta_days + 1)]

        for instrument, values in data.items():
            for date in dates:
                if not next((x for x in values if x['date'] == date), False):
                    data[instrument].append({'length': 0, 'date': date})
            data[instrument].sort(key=lambda k: k['date'])

        return PracticeGraphData(data, dates)

    """
    TASKS
    """

    def launch_task(self, name: str, description: str, *args, **kwargs):
        export_practices.delay(self, name, description, *args, **kwargs)

    def get_tasks_in_progress(self):
        return Task.objects.filter(user_profile=self, complete=False).all()

    def get_task_in_progress(self, name):
        return Task.objects.filter(name=name, user_profile=self, complete=False).first()

    """
    TOKENS
    """

    def generate_token(self, token_type: TokenType, expires_in=600) -> str:
        serializer = Serializer(SECRET_KEY, expires_in)
        return serializer.dumps({token_type.value: self.user.pk}).decode('utf-8')

    @staticmethod
    def reset_password(token: str, new_password: str) -> bool:
        user = get_user_from_token(token, TokenType.RESET)
        if not user:
            return False

        user.set_password(new_password)
        user.save()
        return True

    def confirm(self, token: str) -> bool:
        user = get_user_from_token(token, TokenType.CONFIRM)
        if not user or user.pk != self.user.pk:
            return False

        user.is_active = True
        user.save()
        return True


def get_user_from_token(token: str, token_type: TokenType) -> User:
    try:
        serializer = Serializer(SECRET_KEY)
        data = serializer.loads(token.encode('utf-8'))
        user_pk = data.get(token_type.value)
        return User.objects.get(pk=user_pk) if user_pk else None
    except BadSignature:
        return None


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.email = instance.email.lower()

        email_preferences = EmailPreferences.objects.create(features=True, practicing=True, promotions=True)
        instance.email_preferences = email_preferences

    instance.profile.save()
