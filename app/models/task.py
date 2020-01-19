import rq
import redis

from django.db import models
from django_rq import job

from musicavis.settings import BROKER_URL


class Task(models.Model):
    id = models.CharField(max_length=36, primary_key=True, unique=True)
    name = models.CharField(max_length=128, db_index=True, null=False)
    description = models.CharField(max_length=128)
    user_profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)

    def get_rq_job(self):
        try:
            return job.Job.fetch(self.id, connection=BROKER_URL)
        except (redis.exceptions.RedsError, rq.exceptions.NoSuchJobError):
            return None

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job else 100

    def __eq__(self, other):
        return (self.id == other.id and
                self.name == other.name and
                self.description == other.description and
                self.user_profile == other.user_profile and
                self.complete == other.complete)
