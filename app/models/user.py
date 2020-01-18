import json
import math
from hashlib import md5
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.utils import timezone
import django_rq

from .validators import UsernameValidator
from .practice import Practice, Instrument
from .email_preferences import EmailPreferences
from .notification import Notification
from .task import Task
from ..backend.utils.tasks import export_practices
from ..backend.utils.enums import FileType, NewLine
from ..backend.utils.export import ExportPractices
from ..backend.dashboard.stats import PracticeStats
from ..backend.utils.namedtuples import PracticeGraphData


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    practices = models.ManyToManyField('Practice')
    email_preferences = models.ForeignKey('EmailPreferences', on_delete=models.CASCADE)
    notifications = models.ManyToManyField('Notification')

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.email = self.email.lower()

        email_preferences = EmailPreferences(features=True, practicing=True, promotions=True)
        email_preferences.save()
        self.email_preferences = email_preferences

        return super().save(*args, **kwargs)

    """
    GENERAL
    """

    def verify_password(self, password: str) -> bool:
        return check_password(password, self.password)

    def update_email_preferences(self, accept_features: bool, accept_practicing: bool, accept_promotions: bool):
        self.email_preferences.features = accept_features
        self.email_preferences.practicing = accept_practicing
        self.email_preferences.promotions = accept_promotions

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def add_notification(self, name, data):
        self.notifications.all().filter(name=name).delete()
        notification = Notification(name=name, payload_json=json.dumps(data), user_object=self)
        notification.save()
        self.notifications.add(notification)
        return notification

    def __str__(self):
        return self.username

    """
    PRACTICE
    """

    def new_practice(self, instrument_name: str) -> Practice:
        instrument = Instrument.objects.filter(name=instrument_name).first()
        if instrument is None:
            instrument = Instrument(name=instrument_name)
            instrument.save()

        practice = Practice(user_object=self, instrument=instrument)
        practice.save()
        self.practices.add(practice)
        return practice

    def delete_practice(self, practice: Practice):
        if practice.user_object == self:
            practice.delete()

    def export_practices(self, os: NewLine, filetype: FileType):
        export_practices = ExportPractices(self.username, self.practices.all(), os)
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
        export_practices.delay(self, name, description)

    def get_tasks_in_progress(self):
        return Task.objects.filter(user_object=self, complete=False).all()

    def get_task_in_progress(self, name):
        return Task.objects.filter(name=name, user_object=self, complete=False).first()
