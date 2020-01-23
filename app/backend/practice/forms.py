from decimal import Decimal

from django import forms

from app.models.practice import Practice, Goal, Improvement, Positive, Exercise
from app.backend.utils.namedtuples import ExerciseData


class NewPracticeForm(forms.Form):
    instrument = forms.ChoiceField(choices=[])

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instrument'].choices = choices


class ExerciseForm(forms.Form):
    name = forms.CharField()
    bpm_start = forms.IntegerField(max_value=400, min_value=30, initial=60)
    bpm_bpm_endstart = forms.IntegerField(max_value=400, min_value=30, initial=60)
    minutes = forms.DecimalField(decimal_places=2, min_value=0, initial=5.00)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.name.data:
            self.name.data = self.name.data.title()


class NameForm(forms.Form):
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields['name'].value:
            self.fields['name'].value = self.fields['name'].value.capitalize()


class PracticeForm(forms.ModelForm):

    class Meta:
        model = Practice
        exclude = ['user_profile']

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance')
        initial = kwargs.setdefault('initial', {})
        initial['notes'] = instance.notes
        self.data = kwargs.get('data', None)
        super().__init__(*args, **kwargs)
        self.fields['notes'].widget.attrs.update({'class': 'textarea', 'placeholder': 'Text lines...', 'rows': 5})

        self.__add_fields('goal', instance.goals.all(), 'Goal...')
        self.__add_exercise_fields(instance.exercises.all())
        self.__add_fields('positive', instance.positives.all(), 'Positive...')
        self.__add_fields('improvement', instance.improvements.all(), 'What to improve...')

    def __add_fields(self, label, components, placeholder=''):
        for i in range(len(components) + 1):
            field_name = f'{label}_{i}'
            self.fields[field_name] = forms.CharField(required=False)
            try:
                self.initial[field_name] = components[i].name
            except IndexError:
                self.initial[field_name] = ''

        for field_name in self.fields:
            if field_name.startswith(f'{label}_'):
                self.fields[field_name].widget.attrs.update({'class': 'input', 'placeholder': placeholder})
            self.fields[field_name].required = False

    def __add_exercise_fields(self, exercises):
        labels = ['name', 'bpm_start', 'bpm_end', 'minutes']
        for idx, exercise in enumerate(exercises):
            values = [exercise.name, exercise.bpm_start, exercise.bpm_end, exercise.minutes]
            for label, value in zip(labels, values):
                field_name = f'exercise_{idx}_{label}'
                self.fields[field_name] = forms.CharField(required=False)
                self.initial[field_name] = value

                if label in ['bpm_start', 'bpm_end', 'minutes']:
                    self.fields[field_name].widget = forms.NumberInput()
                    self.fields[field_name].widget.attrs.update({'class': 'input input-change'})
                else:
                    self.fields[field_name].widget.attrs.update({'class': 'input', 'placeholder': 'Exercise name...'})

                if label == 'minutes':
                    self.fields[field_name].widget.attrs.update({'step': '0.5', 'min': '1.0'})
                elif label == 'bpm_start':
                    self.fields[field_name].widget.attrs.update({'step': '1.0', 'min': '30', 'max': '400'})
                elif label == 'bpm_end':
                    self.fields[field_name].widget.attrs.update({'step': '1.0', 'min': '30', 'max': '400'})

        next_idx = len(exercises)
        for label in labels:
            field_name = f'exercise_{next_idx}_{label}'
            self.fields[field_name] = forms.CharField(required=False)

            if label in ['bpm_start', 'bpm_end', 'minutes']:
                self.fields[field_name].widget = forms.NumberInput()
                self.fields[field_name].widget.attrs.update({'class': 'input input-change'})
            else:
                self.fields[field_name].widget.attrs.update({'class': 'input', 'placeholder': 'Exercise name...'})

            if label == 'minutes':
                self.fields[field_name].widget.attrs.update({'step': '0.5', 'value': '5.0', 'min': '1.0'})
            elif label == 'bpm_start':
                self.fields[field_name].widget.attrs.update({'step': '1.0', 'value': '60', 'min': '30', 'max': '400'})
            elif label == 'bpm_end':
                self.fields[field_name].widget.attrs.update({'step': '1.0', 'value': '80', 'min': '30', 'max': '400'})

    def clean(self):
        self.__field_cleaning('goal')
        self.__field_cleaning('positive')
        self.__field_cleaning('improvement')
        self.__field_cleaning_exercise()

    def __field_cleaning(self, label):
        self.cleaned_data[f'{label}s'] = set()
        i = self.__field_cleaning_with_dict(0, self.cleaned_data, label)
        if self.data:
            self.__field_cleaning_with_dict(i, self.data, label)

    def __field_cleaning_with_dict(self, i, data, label):
        components = set()
        field_name = f'{label}_{i}'
        while data.get(field_name):
            component = data[field_name]
            if component in components:
                self.add_error(field_name, 'Duplicate')
            else:
                components.add(component)

            i += 1
            field_name = f'{label}_{i}'

        self.cleaned_data[f'{label}s'] = self.cleaned_data[f'{label}s'].union(components)
        return i

    def __field_cleaning_exercise(self):
        self.cleaned_data['exercises'] = set()
        i = self.__field_cleaning_exercises_with_dict(0, self.cleaned_data)
        if self.data:
            self.__field_cleaning_exercises_with_dict(i, self.data)

    def __field_cleaning_exercises_with_dict(self, i, data):
        components = set()
        while data.get(f'exercise_{i}_name'):
            component = ExerciseData(name=data[f'exercise_{i}_name'],
                                     bpm_start=int(data[f'exercise_{i}_bpm_start']),
                                     bpm_end=int(data[f'exercise_{i}_bpm_end']),
                                     minutes=Decimal(str(data[f'exercise_{i}_minutes'])))

            if component in components:
                self.add_error('exercise', 'Duplicate')
            else:
                components.add(component)
            i += 1

        self.cleaned_data['exercises'] = self.cleaned_data['exercises'].union(components)
        return i

    def save(self, instance):
        instance.notes = self.cleaned_data['notes']

        self.__update_field('goals', instance)
        self.__update_field('improvements', instance)
        self.__update_field('positives', instance)
        self.__update_field('exercises', instance)

        instance.save()

    def __update_field(self, field_name, instance):
        if field_name == 'goals':
            objects = instance.goals
            model = Goal
        elif field_name == 'positives':
            objects = instance.positives
            model = Positive
        elif field_name == 'improvements':
            objects = instance.improvements
            model = Improvement
        else:
            objects = instance.exercises
            model = Exercise

        for obj in objects.all():
            objects.remove(obj)

        if field_name == 'exercises':
            for exercise_tuple in self.cleaned_data[field_name]:
                name = exercise_tuple.name
                bpm_start = exercise_tuple.bpm_start
                bpm_end = exercise_tuple.bpm_end
                minutes = exercise_tuple.minutes

                obj = Exercise.objects.filter(name=name, bpm_start=bpm_start, bpm_end=bpm_end, minutes=minutes).first()
                if not obj:
                    obj = model.objects.create(name=name, bpm_start=bpm_start, bpm_end=bpm_end, minutes=minutes)
                objects.add(obj)
        else:
            for name in self.cleaned_data[field_name]:
                obj = model.objects.filter(name=name).first()
                if not obj:
                    obj = model.objects.create(name=name)
                objects.add(obj)

    def get_goal_fields(self):
        for field_name in self.fields:
            if field_name.startswith('goal_'):
                yield self[field_name]

    def get_exercise_fields(self):
        indexes = []
        for field_name in self.fields:
            if field_name.startswith('exercise_'):
                idx = int(field_name.split('_')[1])
                if idx not in indexes:
                    indexes.append(idx)
                    yield (self[f'exercise_{idx}_name'],
                           self[f'exercise_{idx}_bpm_start'],
                           self[f'exercise_{idx}_bpm_end'],
                           self[f'exercise_{idx}_minutes'])

    def get_positive_fields(self):
        for field_name in self.fields:
            if field_name.startswith('positive_'):
                yield self[field_name]

    def get_improvement_fields(self):
        for field_name in self.fields:
            if field_name.startswith('improvement_'):
                yield self[field_name]
