from calendar import HTMLCalendar, SUNDAY

from django.utils import timezone
from django.urls import reverse

from app.models.practice import Practice


class PracticeListCalendar(HTMLCalendar):

    def __init__(self, date, practices):
        super().__init__(firstweekday=SUNDAY)
        self.year = date.year
        self.month = date.month
        self.practices = practices

    def formatmonth(self, withyear=True):
        cal = (f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
               f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
               f'{self.formatweekheader()}\n')

        practices = self.practices.filter(date__year__gte=self.year, date__month__gte=self.month)
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, practices)}\n'
        return cal

    def formatweek(self, theweek, practices):
        week = ''.join([self.formatday(d, practices) for d, weekday in theweek])
        return f'<tr>{week}</tr>'

    def formatday(self, day, practices):
        if day != 0:
            practices_per_day = practices.filter(date__day=day)
            day_practices = ''
            for practice in practices_per_day:
                url = reverse('app:practice.session', args=[practice.pk])
                day_practices += (
                    f'<li class="practice-session-calendar">'
                    f'<a href="{url}">'
                    f'<div>{practice.instrument.name.title()}</div>'
                    f'<div class="practice-session-time">{practice.format_total_practice_time()}</div>'
                    '</a></li>'
                )
            return f'<td><span class="date">{day}</span><ul>{day_practices}</ul></td>'
        return '<td></td>'
