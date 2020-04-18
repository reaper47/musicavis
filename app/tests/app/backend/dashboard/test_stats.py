from decimal import Decimal
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from app.backend.dashboard.stats import PracticeStats
from app.models.practice import Practice, Instrument, Exercise
from app.tests.conftest import create_user, delete_users

AN_INSTRUMENT_NAME = "bob"
OTHER_INSTRUMENT_NAME = "bobby"


def stats():
    user = create_user()
    instrument1 = Instrument.objects.create(name=AN_INSTRUMENT_NAME)
    instrument2 = Instrument.objects.create(name=OTHER_INSTRUMENT_NAME)

    practice1 = Practice.objects.create(
        user_profile=user.profile, date=timezone.now(), instrument=instrument1
    )
    practice1.exercises.set(
        [
            Exercise.objects.create(
                name="C-Arpeggio", bpm_start=60, bpm_end=80, minutes=Decimal("5")
            ),
            Exercise.objects.create(
                name="D-Arpeggio", bpm_start=60, bpm_end=75, minutes=Decimal("5")
            ),
            Exercise.objects.create(
                name="Chord Progressions",
                bpm_start=80,
                bpm_end=80,
                minutes=Decimal("10"),
            ),
            Exercise.objects.create(
                name="Psychroptic", bpm_start=80, bpm_end=80, minutes=Decimal("20")
            ),
        ]
    )

    practice2 = Practice.objects.create(
        user_profile=user.profile,
        date=timezone.now() - timedelta(days=1),
        instrument=instrument2,
    )
    practice2.exercises.set(
        [
            Exercise.objects.create(
                name="D-Arpeggio", bpm_start=60, bpm_end=80, minutes=Decimal("5")
            ),
            Exercise.objects.create(
                name="E-Arpeggio", bpm_start=50, bpm_end=55, minutes=Decimal("7")
            ),
            Exercise.objects.create(
                name="Downpicking", bpm_start=80, bpm_end=80, minutes=Decimal("10")
            ),
            Exercise.objects.create(
                name="Kalmah", bpm_start=80, bpm_end=80, minutes=Decimal("22")
            ),
        ]
    )

    practice3 = Practice.objects.create(
        user_profile=user.profile,
        date=timezone.now() - timedelta(days=2),
        instrument=instrument1,
    )
    practice3.exercises.set(
        [
            Exercise.objects.create(
                name="C-Arpeggio", bpm_start=60, bpm_end=85, minutes=Decimal("8")
            ),
            Exercise.objects.create(
                name="F-Arpeggio", bpm_start=80, bpm_end=75, minutes=Decimal("5")
            ),
            Exercise.objects.create(
                name="Chord Progressions",
                bpm_start=80,
                bpm_end=80,
                minutes=Decimal("10"),
            ),
            Exercise.objects.create(
                name="Psychroptic", bpm_start=80, bpm_end=80, minutes=Decimal("20")
            ),
        ]
    )

    practice4 = Practice.objects.create(
        user_profile=user.profile,
        date=timezone.now() - timedelta(days=3),
        instrument=instrument2,
    )
    practice4.exercises.set(
        [
            Exercise.objects.create(
                name="G-Arpeggio", bpm_start=90, bpm_end=95, minutes=Decimal("5")
            ),
            Exercise.objects.create(
                name="D-Arpeggio", bpm_start=60, bpm_end=75, minutes=Decimal("5")
            ),
            Exercise.objects.create(
                name="Alternate Picking",
                bpm_start=80,
                bpm_end=80,
                minutes=Decimal("10"),
            ),
            Exercise.objects.create(
                name="Psychroptic", bpm_start=80, bpm_end=80, minutes=Decimal("25")
            ),
        ]
    )

    practice5 = Practice.objects.create(
        user_profile=user.profile,
        date=timezone.now() - timedelta(days=4),
        instrument=instrument1,
    )
    practice5.exercises.set(
        [
            Exercise.objects.create(
                name="C-Arpeggio", bpm_start=60, bpm_end=80, minutes=Decimal("15")
            ),
            Exercise.objects.create(
                name="B-Arpeggio", bpm_start=65, bpm_end=70, minutes=Decimal("15")
            ),
            Exercise.objects.create(
                name="Sweep Picking", bpm_start=80, bpm_end=80, minutes=Decimal("15")
            ),
            Exercise.objects.create(
                name="Kalmah", bpm_start=80, bpm_end=80, minutes=Decimal("20")
            ),
        ]
    )

    return PracticeStats([practice1, practice2, practice3, practice4, practice5])


class StatsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stats = stats()

    @classmethod
    def tearDownClass(cls):
        delete_users()
        Instrument.objects.get(name="bob").delete()
        Instrument.objects.get(name="bobby").delete()

    def test_total_practice_time(self):
        time_expected = 237

        time = self.stats.total_practice_time

        self.assertEqual(time_expected, time)

    def test_avg_practice_time(self):
        time_expected = 47

        time = self.stats.avg_practice_time

        self.assertEqual(time_expected, time)

    def test_median_practice_time(self):
        time_expected = 44

        time = self.stats.median_practice_time

        self.assertEqual(time_expected, time)

    def test_max_practice_time(self):
        max_time_expected = 65

        max_time = self.stats.max_practice_time

        self.assertEqual(max_time_expected, max_time)

    def test_min_practice_time(self):
        min_time_expected = 40

        min_time = self.stats.min_practice_time

        self.assertEqual(min_time_expected, min_time)

    def test_num_exercises(self):
        num_exercises_expected = 20

        num_exercises = self.stats.num_exercises

        self.assertEqual(num_exercises_expected, num_exercises)

    def test_avg_num_exercises(self):
        avg_num_exercises_expected = 4

        avg_num_exercises = self.stats.avg_num_exercises

        self.assertEqual(avg_num_exercises_expected, avg_num_exercises)

    def test_median_num_exercises(self):
        median_num_exercises_expected = 4

        median_num_exercises = self.stats.median_num_exercises

        self.assertEqual(median_num_exercises_expected, median_num_exercises)

    def test_avg_exercise_length(self):
        avg_exercise_length_expected = Decimal("11.85")

        avg_exercise_length = self.stats.avg_exercise_length

        self.assertEqual(avg_exercise_length_expected, avg_exercise_length)

    def test_median_exercise_length(self):
        median_exercise_length_expected = 10

        median_exercise_length = self.stats.median_exercise_length

        self.assertEqual(median_exercise_length_expected, median_exercise_length)

    def test_most_practiced_instrument(self):
        instrument_expected = AN_INSTRUMENT_NAME.lower()

        instrument = self.stats.most_practiced_instrument

        self.assertEqual(instrument_expected, instrument)

    def test_least_practiced_instrument(self):
        instrument_expected = OTHER_INSTRUMENT_NAME.lower()

        instrument = self.stats.least_practiced_instrument

        self.assertEqual(instrument_expected, instrument)

    def test_return_zero_on_statistics_error(self):
        stats = PracticeStats([])

        results = [
            stats.avg_practice_time,
            stats.median_practice_time,
            stats.max_practice_time,
            stats.min_practice_time,
            stats.num_exercises,
            stats.avg_num_exercises,
            stats.median_num_exercises,
            stats.avg_exercise_length,
            stats.median_exercise_length,
        ]

        for result in results:
            self.assertEqual(result, 0)
