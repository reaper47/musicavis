from decimal import Decimal

from django.test import TestCase

from app.backend.practice.forms import PracticeForm
from app.tests.conftest import create_user, delete_users, delete_everything
from app.models.practice import Goal, Positive, Improvement, Exercise
from app.backend.utils.namedtuples import ExerciseData

A_GOAL_NAME = 'A nice goal'
OTHER_GOAL_NAME = 'Another nice goal'
A_POSITIVE_NAME = 'A nice positive'
OTHER_POSITIVE_NAME = 'Other nice positive'
AN_IMPROVEMENT_NAME = 'A nice improvement'
OTHER_IMPROVEMENT_NAME = 'Other nice improvement'
AN_EXERCISE_NAME = 'A nice exercise'
OTHER_EXERCISE_NAME = 'A nice exercise'
A_BPM_START = 60
OTHER_BPM_START = 100
A_BPM_END = 80
OTHER_BPM_END = 120
SOME_MINUTES = Decimal('10.00')
SOME_OTHER_MINUTES = Decimal('15.50')
SOME_NOTES = 'Some nice notes'

data = {
    'notes': SOME_NOTES,
    'goal_0': A_GOAL_NAME,
    'goal_1': '',
    'exercise_0_name': AN_EXERCISE_NAME,
    'exercise_0_bpm_start': A_BPM_START,
    'exercise_0_bpm_end': A_BPM_END,
    'exercise_0_minutes': SOME_MINUTES,
    'exercise_1_name': '',
    'exercise_1_bpm_start': '',
    'exercise_1_bpm_end': '',
    'exercise_1_minutes': '',
    'positive_0': A_POSITIVE_NAME,
    'positive_1': '',
    'improvement_0': AN_IMPROVEMENT_NAME,
    'improvement_1': ''
}

other_data = {
    'notes': SOME_NOTES,
    'goal_0': A_GOAL_NAME,
    'goal_1': OTHER_GOAL_NAME,
    'goal_2': '',
    'exercise_0_name': AN_EXERCISE_NAME,
    'exercise_0_bpm_start': A_BPM_START,
    'exercise_0_bpm_end': A_BPM_END,
    'exercise_0_minutes': SOME_MINUTES,
    'exercise_1_name': OTHER_EXERCISE_NAME,
    'exercise_1_bpm_start': OTHER_BPM_START,
    'exercise_1_bpm_end': OTHER_BPM_END,
    'exercise_1_minutes': SOME_OTHER_MINUTES,
    'exercise_2_name': '',
    'exercise_2_bpm_start': '',
    'exercise_2_bpm_end': '',
    'exercise_2_minutes': '',
    'positive_0': A_POSITIVE_NAME,
    'positive_1': OTHER_POSITIVE_NAME,
    'positive_2': '',
    'improvement_0': AN_IMPROVEMENT_NAME,
    'improvement_1': OTHER_IMPROVEMENT_NAME,
    'improvement_2': ''
}


class PracticeFormsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        delete_everything()
        cls.a_user = create_user()

    @classmethod
    def tearDownClass(cls):
        delete_everything()
        delete_users()

    def setUp(self):
        self.practice = self.a_user.profile.new_practice('cheese')
        self.practice.save()

    def tearDown(self):
        self.a_user.profile.practices.all().delete()

    def test_init_empty_practice(self):
        """
        WHEN creating a form from an empty practice
        THEN display a form with one empty input for each field
        """
        data_expected = {
            'notes': '',
            'goals': set(),
            'exercises': set(),
            'improvements': set(),
            'positives': set()
         }

        form = PracticeForm({}, instance=self.practice)
        form.is_valid()

        fields = ['notes', 'goals', 'exercises', 'positives', 'improvements']
        for field in fields:
            self.assertEqual(form.cleaned_data[field], data_expected[field])

    def test_init_complete_practice_data(self):
        """
        GIVEN a complete practice
        WHEN creating a practice form
        THEN all the practice's data is displayed appropriately
        """
        make_empty_practice(self.practice)
        data_expected = {
            'notes': SOME_NOTES,
            'goals': {A_GOAL_NAME},
            'exercises': {ExerciseData(name=AN_EXERCISE_NAME,
                                       bpm_start=A_BPM_START,
                                       bpm_end=A_BPM_END,
                                       minutes=SOME_MINUTES)},
            'improvements': {AN_IMPROVEMENT_NAME},
            'positives': {A_POSITIVE_NAME}
         }

        form = PracticeForm(data, instance=self.practice)
        form.is_valid()

        for field in data_expected.keys():
            self.assertEqual(form.cleaned_data[field], data_expected[field])

    def test_save_complete_practice(self):
        """
        GIVEN a practice form completely filled out
        WHEN the form is saved
        THEN the database is updated correctly
        """
        form = PracticeForm(data, instance=self.practice)
        form.is_valid()
        form.save(self.practice)

        goal = Goal.objects.filter(name=A_GOAL_NAME).first()
        improvement = Improvement.objects.filter(name=AN_IMPROVEMENT_NAME).first()
        positive = Positive.objects.filter(name=A_POSITIVE_NAME).first()
        exercise = Exercise.objects.filter(name=AN_EXERCISE_NAME, bpm_start=A_BPM_START,
                                           bpm_end=A_BPM_END, minutes=SOME_MINUTES).first()
        self.assertEqual(list(self.practice.goals.all()), [goal])
        self.assertEqual(list(self.practice.improvements.all()), [improvement])
        self.assertEqual(list(self.practice.positives.all()), [positive])
        self.assertEqual(list(self.practice.exercises.all()), [exercise])

    def test_save_complete_practice_multiple(self):
        """
        GIVEN a practice form completely filled out with multiple goals, positives, improvements, and exercises
        WHEN the form is saved
        THEN the database is updated correctly
        """
        Exercise.objects.all().delete()
        form = PracticeForm(data=other_data, instance=self.practice)
        form.is_valid()
        form.save(self.practice)

        goals = list(Goal.objects.all())
        improvements = list(Improvement.objects.all())
        positives = list(Positive.objects.all())
        exercises = list(Exercise.objects.all())
        for x in [goals, improvements, positives, exercises]:
            self.assertEqual(len(x), 2, x[0].__class__)
        self.assertEqual(list(self.practice.goals.all()), goals)
        self.assertEqual(list(self.practice.improvements.all()), improvements)
        self.assertEqual(list(self.practice.positives.all()), positives)
        self.assertEqual(list(self.practice.exercises.all()), exercises)

    def test_save_complete_practice_duplicates(self):
        """
        GIVEN a practice form completely filled out with duplicate goals, positives, improvements, and exercises
        WHEN the form is saved
        THEN saved form has no duplicates
        """
        Exercise.objects.all().delete()
        form = PracticeForm(data=other_data, instance=self.practice)
        form.is_valid()
        form.save(self.practice)

        goals = list(Goal.objects.all())
        improvements = list(Improvement.objects.all())
        positives = list(Positive.objects.all())
        exercises = list(Exercise.objects.all())
        for x in [goals, improvements, positives, exercises]:
            self.assertEqual(len(x), 2, x[0].__class__)
        self.assertEqual(list(self.practice.goals.all()), goals)
        self.assertEqual(list(self.practice.improvements.all()), improvements)
        self.assertEqual(list(self.practice.positives.all()), positives)
        self.assertEqual(list(self.practice.exercises.all()), exercises)


def make_empty_practice(practice):
    goal = Goal(name=A_GOAL_NAME)
    goal.save()
    practice.goals.add(goal)

    exercise = Exercise(name=AN_EXERCISE_NAME, bpm_start=A_BPM_START, bpm_end=A_BPM_END, minutes=SOME_MINUTES)
    exercise.save()
    practice.exercises.add(exercise)

    positive = Positive(name=A_POSITIVE_NAME)
    positive.save()
    practice.positives.add(positive)

    improvement = Improvement(name=AN_IMPROVEMENT_NAME)
    improvement.save()
    practice.improvements.add(improvement)

    practice.notes = SOME_NOTES

    practice.save()
