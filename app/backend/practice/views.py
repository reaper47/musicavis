import calendar

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.utils.html import mark_safe

from app.models.practice import Instrument
from app.backend.practice.forms import NewPracticeForm, PracticeForm
from app.backend.utils.calendar import PracticeListCalendar

PRACTICES_PER_PAGE = 12


@login_required
def new_view(request):
    instruments = request.user.profile.instruments_practiced.all()
    num_instruments = len(instruments)

    if num_instruments == 1:
        practice = request.user.profile.new_practice(instruments[0].name)
        return redirect(reverse('app:practice.session', args=[practice.id]))

    instruments = instruments if num_instruments > 1 else Instrument.objects.all()
    choices = sorted([(x.name.lower(), x.name.title()) for x in instruments])
    form = NewPracticeForm(choices)

    if request.method == 'POST':
        data = request.POST.copy()
        form = NewPracticeForm(choices=choices, data=data)
        if form.is_valid():
            practice = request.user.profile.new_practice(data['instrument'].lower())
            return redirect(reverse('app:practice.session', args=[practice.id]))

    args = dict(title='New Practice Session', form=form)
    return render(request, 'practice/new_practice.html', args)


@login_required
def session_view(request, practice_id):
    practice = get_object_or_404(request.user.profile.practices, pk=practice_id)
    form = PracticeForm(instance=practice)
    form_mobile = PracticeForm(instance=practice, prefix='mobile')

    if request.method == 'POST':
        data = request.POST.dict().copy()
        form = PracticeForm(data=data, instance=practice)
        if form.is_valid():
            form.save(practice)
            return JsonResponse({'status_code': 200, 'toast': 'Changes have been saved.'})
        return JsonResponse({'status_code': 400, 'toast': 'Error saving changes.'})
    elif request.method == 'DELETE':
        messages.info(request, f'[{practice.instrument.name.title()}] Practice #{practice.pk} successfully deleted.')
        practice.delete()
        return HttpResponseRedirect(reverse('app:practice.list_past_practices'))

    args = dict(title=f'Practice #{practice.id} ({practice.instrument.name})',
                instrument_name=practice.instrument.name.title(),
                practice_date=practice.date.strftime('%d/%m/%Y'),
                goals=form.fields['goals'],
                practice=practice,
                practice_session_url=reverse('app:practice.session', args=[practice.pk]),
                form=form,
                isSession=True,
                form_mobile=form_mobile,
                signatures=['2/4', '3/4', '4/4', '6/8', '9/8', '12/8'],
                divisions=[(0, 'Quarter note (♩)'), (1, 'Eighth note (♪)'),
                           (2, 'Sixteenth note (♬)'), (3, 'Thirty-second note 𝅘𝅥𝅰')],
                timer_components=[('Hours:', 'num-hours', 24, 0, 0), ('Minutes:', 'num-minutes', 60, 0, 5),
                                  ('Seconds:', 'num-seconds', 60, 0, 0)])
    return render(request, 'practice/session.html', args)


@login_required
def list_past_practices_view(request):
    date = timezone.now()
    months = list(calendar.month_abbr)

    try:
        referer = request.headers['Referer'].split('?')[1].split('&')
        params = dict(year=int(referer[1].split('=')[1]),
                      month=int(months.index(referer[0].split('=')[1][:3])),
                      flow=referer[2].split('=')[1])

        if params['flow'] == 'next':
            month = 1 if params['month'] == 12 else params['month'] + 1
            year = params['year'] if params['month'] < 12 else params['year'] + 1
        else:
            month = 12 if params['month'] == 1 else params['month'] - 1
            year = params['year'] if params['month'] > 1 else params['year'] - 1

        date = date.replace(month=month, year=year)
    except (IndexError, KeyError):
        pass

    cal = PracticeListCalendar(date, request.user.profile.practices.all()).formatmonth()

    args = dict(title='Past Practice Sessions',
                url_practice_list=reverse('app:practice.list_past_practices'),
                calendar=mark_safe(cal))
    return render(request, 'practice/list.html', args)
