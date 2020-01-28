from django.test import TestCase

import app.tests.app.backend.practice.test_dtos as dtos
from app.backend.practice.dtos import PracticeDTO
from app.models.practice import Goal, Improvement, Positive, Exercise, Practice
from app.tests.conftest import create_user, create_user_with_a_practice, AN_INSTRUMENT, delete_users, delete_everything


class PracticeModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        delete_everything()
        cls.a_user_with_a_practice = create_user_with_a_practice()

    @classmethod
    def tearDownClass(cls):
        delete_users()

    def test_models_equality_name_property(self):
        """
        GIVEN two Goal, two Improvement, and two Positive with the same name attribute
        WHEN they are compared
        THEN they are equal
        """
        a_goal, other_goal = Goal(name='a goal'), Goal(name='a goal')
        an_improvement, other_improvement = Improvement(name='an improvement'), Improvement(name='an improvement')
        a_positive, other_positive = Positive(name='a positive'), Positive(name='a positive')

        is_goal_equal = a_goal == other_goal
        is_improvement_equal = an_improvement == other_improvement
        is_positive_equal = a_positive == other_positive

        assert is_goal_equal and is_improvement_equal and is_positive_equal

    def test_format_total_practice_time(self):
        """
        GIVEN a practice session with 5 exercises each lasting 25 minutes
        WHEN the total practice time is formatted
        THEN the time is formatted as hours-minutes
        """
        exercises = [Exercise(name=chr(ord('A') + i), bpm_start=i, bpm_end=i, minutes=25) for i in range(5)]
        for exercise in exercises:
            exercise.save()
        practice = create_user().profile.new_practice(AN_INSTRUMENT)
        practice.exercises.add(*exercises)
        formatted_time_expected = '2h05'

        formatted_time_actual = practice.format_total_practice_time()

        assert formatted_time_expected == formatted_time_actual

    def test_format_total_practice_time_no_exercises(self):
        """
        GIVEN a practice with no exercises
        WHEN the total practice time is formatted
        THEN the time is formatted but null
        """
        practice = create_user().profile.new_practice(AN_INSTRUMENT)
        formatted_time_expected = '0h00'

        formatted_time_actual = practice.format_total_practice_time()

        assert formatted_time_expected == formatted_time_actual

    def test_update_model_new_practice(self):
        """
        GIVEN a freshly-created practice session
        WHEN the practice session in the database is updated with the model
        THEN update the practice correctly
        """
        old_model = self.a_user_with_a_practice.profile.practices.first()
        new_practice = PracticeDTO(
            [Goal(name=dtos.A_GOAL)],
            [Exercise(name=dtos.AN_EXERCISE, bpm_start=dtos.A_BPM, bpm_end=dtos.A_BPM, minutes=dtos.SOME_MINUTES)],
            [Positive(name=dtos.A_POSITIVE)],
            [Improvement(name=dtos.AN_IMPROVEMENT)],
            notes=dtos.A_NOTE
        )
        old_model.update_model(new_practice)

        practice = Practice.objects.filter(pk=old_model.pk).first()
        updated_model = PracticeDTO(
            list(practice.goals.all()),
            list(practice.exercises.all()),
            list(practice.positives.all()),
            list(practice.improvements.all()),
            dtos.A_NOTE
        )
        self.assertEqual(new_practice, updated_model)

    def test_models_to_string(self):
        """
        GIVEN an instance of every model
        WHEN each model is stringified
        THEN each model is formatted as intended
        """
        practice = self.a_user_with_a_practice.profile.practices.first()
        goal = Goal.objects.create(name='test')
        models = [(practice, f'#{practice.pk} - {practice.date}'),
                  (Exercise(name='test'), f'test - [None,None] (None)'),
                  (practice.instrument, f'{practice.instrument.name}'),
                  (goal, '#18 - test'),
                  (Improvement(name='test'), 'test'),
                  (Positive(name='test'), 'test')]

        for model, expected_string in models:
            self.assertEqual(str(model), expected_string)

    def test_total_practice_time(self):
        """
        GIVEN a profile with 2 exercises,
        WHEN the 'total_practice_time' property is accessed
        THEN the total practice time is summed
        """
        length1, length2 = 50, 70
        practice = self.a_user_with_a_practice.profile.practices.first()
        exercises = [('C', 80, 75, length1), ('D', 95, 70, length2)]
        for name, start, end, min in exercises:
            exercise = Exercise.objects.create(name=name, bpm_start=start, bpm_end=end, minutes=min)
            practice.exercises.add(exercise)

        length = self.a_user_with_a_practice.profile.practices.first().length

        self.assertEqual(length, length1 + length2)
