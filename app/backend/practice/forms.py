from typing import List

from django import forms

from app.models.practice import Practice


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
            fields = ['notes', 'goals', 'exercises', 'positives', 'improvements']

    notes = forms.CharField(label='Additional Notes', widget=forms.TextInput(), required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)
        self.fields['notes'] = instance.notes
        self.__add_fields('goal', instance.goals.all())
        self.__add_fields('exercise', instance.exercises.all())
        self.__add_fields('positive', instance.positives.all())
        self.__add_fields('improvement', instance.improvements.all())

    def __add_fields(self, label, components):
        for i in range(len(components) + 1):
            field_name = f'{label}_{i}'
            self.fields[field_name] = forms.CharField(required=False)
            try:
                self.initial[field_name] = components[i].name
            except IndexError:
                self.initial[field_name] = ''

        field_name = f'{label}_{len(components) + 1}'
        self.fields[field_name] = forms.CharField(required=False)

    def clean(self):
        self.__field_cleaning('goal')
        self.__field_cleaning('exercise')
        self.__field_cleaning('positive')
        self.__field_cleaning('improvement')

    def __field_cleaning(self, label):
        components = set()
        i = 0
        field_name = f'{label}_{i}'
        while self.cleaned_data.get(field_name):
           component = self.cleaned_data[field_name]
           if component in components:
               self.add_error(field_name, 'Duplicate')
           else:
               components.add(interest)
           i += 1
           field_name = f'{label}_{i}'

        self.cleaned_data[f'{label}s'] = components

    def save(self):
        practice = self.instance
        practice.notes = self.cleaned_data['notes']

        practice.interest_set.all().delete()
        #for goal in self.cleaned_data['goals']:
        #   Goal.objects.create(
        #       profile=profile,
        #       interest=interest,
        #   )

    def get_goal_fields(self):
        for field_name in self.fields:
            if field_name.startswith('goal_'):
                yield self[field_name]

    def get_exercise_fields(self):
        for field_name in self.fields:
            if field_name.startswith('exercise_'):
                yield self[field_name]

    def get_positive_fields(self):
        for field_name in self.fields:
            if field_name.startswith('positive_'):
                yield self[field_name]

    def get_improvement_fields(self):
        for field_name in self.fields:
            if field_name.startswith('improvement_'):
                yield self[field_name]


