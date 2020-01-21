from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from app.models.practice import Practice, Instrument
from app.backend.practice.forms import NewPracticeForm, PracticeForm


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
    practice = get_object_or_404(Practice, pk=practice_id)
    form = PracticeForm(instance=practice)

    if request.method == 'DELETE':
        messages.info(request, f'[{practice.instrument.name.title()}] Practice #{number} successfully deleted.')
        request.user.profile.delete_practice(number)
        return reverse('app:practice.list_past_practices')
    elif request.method == 'POST':
        model = PracticeDTO.json_to_model(form.data)
        practice.update_model(model)
        model = Practice.query.filter_by(id=number).first()
        jsonable = PracticeDTO.model_to_jsonable(model, 'Changes have been saved.')
        return jsonify(jsonable)

    args = dict(title=f'Practice #{practice.id} ({practice.instrument.name})',
                instrument_name=practice.instrument.name.title(),
                practice_date=practice.date.strftime('%d/%m/%Y'),
                goals=form.fields['goals'],
                practice=practice,
                practice_session_url=reverse('app:practice.session', args=[practice.pk]),
                isSession=True,
                form=form)
    return render(request, 'practice/session.html', args)


@login_required
def list_past_practices_view(request):
    page = request.GET.get('page', 1, type=int)
    practices = request.user.profile.paginate_practices(page, PRACTICES_PER_PAGE)
    next_url = reverse('app:practice.list_past_practices', args=[practices.next_num]) if practices.has_next else None
    prev_url = reverse('app:practice.list_past_practices', args=[practices.prev_num]) if practices.has_prev else None
    args = dict(title='Past Practice Sessions', practices=practices.items, next_url=next_url, prev_url=prev_url)
    return render(request, 'practice/list.html', args)
