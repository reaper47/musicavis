from django.contrib import admin

from .models.practice import Practice, Instrument, Goal, Positive, Improvement, Exercise
from .models.profile import Profile
from .models.notification import Notification
from .models.email_preferences import EmailPreferences
from .models.task import Task


models = [
    (Practice,),
    (Instrument,),
    (Goal,),
    (Improvement,),
    (Profile,),
    (Notification,),
    (EmailPreferences,),
    (Task,),
]

for model in models:
    admin.site.register(*model)
