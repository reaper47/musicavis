import json
from time import time

from django.db import models


class Notification(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    user_object = models.ForeignKey('User', on_delete=models.CASCADE)
    timestamp = models.FloatField(db_index=True, default=time)
    payload_json = models.TextField()

    def get_data(self):
        return json.loads(str(self.payload_json))
