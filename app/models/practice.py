from functools import reduce

from django.db import models
from django.utils import timezone


class Practice(models.Model):
    user_object = models.ForeignKey('User', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE)
    goals = models.ManyToManyField('Goal')
    exercises = models.ManyToManyField('Exercise')
    improvements = models.ManyToManyField('Improvement')
    positives = models.ManyToManyField('Positive')
    notes = models.TextField(null=True, blank=True)

    def format_total_practice_time(self) -> str:
        if not self.exercises.all():
            return '0h00'

        total_num_minutes = reduce(lambda x, y: x + y, [x.minutes for x in self.exercises.all()])
        num_hours = int(total_num_minutes // 60)
        num_minutes = int(total_num_minutes - num_hours * 60)

        return f'{num_hours}h{str(num_minutes).zfill(2)}'

    def update_model(self, updated_model):
        entities = self.__get_entities_from_db(updated_model)

        self.__update_field(self.goals, entities['goals'])
        self.__update_field(self.exercises, entities['exercises'])
        self.__update_field(self.positives, entities['positives'])
        self.__update_field(self.improvements, entities['improvements'])
        self.notes = updated_model.notes

    def __get_entities_from_db(self, model):
        all_entities = {'goals': [], 'exercises': [], 'positives': [], 'improvements': []}

        loops = [('goals', Goal, model.goals),
                 ('positives', Positive, model.positives),
                 ('improvements', Improvement, model.improvements)]

        for key, table, entities in loops:
            entities_in_db = [table.objects.filter(name=x.name).first() for x in entities]
            all_entities[key] = [x if x else y for x, y in zip(entities, entities_in_db)]

        for exercise in model.exercises:
            entity = Exercise.objects.filter(name=exercise.name, bpm_start=exercise.bpm_start,
                                             bpm_end=exercise.bpm_end, minutes=exercise.minutes).first()
            if not entity:
                entity = Exercise(name=exercise.name, bpm_start=exercise.bpm_start,
                                  bpm_end=exercise.bpm_end, minutes=exercise.minutes)
            all_entities['exercises'].append(entity)

        return all_entities

    def __update_field(self, field, objects):
        for x in field.all():
            field.remove(x)

        for x in objects:
            x.save()
            field.add(x)

    @property
    def length(self):
        return sum([x.minutes for x in self.exercises.all()])

    def __str__(self):
        return f'#{self.pk} - {self.date}'


class Exercise(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    bpm_start = models.PositiveSmallIntegerField(null=False, blank=False)
    bpm_end = models.PositiveSmallIntegerField(null=False, blank=False)
    minutes = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return (self.name == other.name and
                self.bpm_start == other.bpm_start and
                self.bpm_end == other.bpm_end and
                self.minutes == other.minutes)

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return f'{self.name} - [{self.bpm_start},{self.bpm_end}] ({self.minutes})'


class Instrument(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Goal(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False, blank=False)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class Improvement(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class Positive(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name
