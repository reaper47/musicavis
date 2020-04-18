from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
import musicavis.settings as settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musicavis.settings")

app = Celery("musicavis", broker=settings.BROKER_URL)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
