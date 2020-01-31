"""
from django.contrib import admin


from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']})
    ]

    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
"""

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
