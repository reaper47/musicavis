from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from app.backend.practice.dtos import PracticeDTO
from app.models.practice import Instrument, Exercise, Goal, Improvement, Positive
from app.tests.conftest import create_user, create_complete_practice, delete_users

A_GOAL = "A nice goal"
AN_EXERCISE = "C-Arpeggio"
OTHER_EXERCISE = "E-Argpeggio"
A_BPM = 60
SOME_MINUTES = Decimal("5.00")
A_POSITIVE = "Budgies are hilarious birds"
AN_IMPROVEMENT = "Reduce intensity to prevent possible injuries"
A_NOTE = "We live in a world full of wonders."


class PracticeDtoTests(TestCase):
    @classmethod
    def setUpClass(cls):
        Instrument.objects.all().delete()
        cls.a_profile = create_user()

    @classmethod
    def tearDownClass(cls):
        delete_users()

    def test_json_to_model_full(self):
        """
        GIVEN a complete json object for a practice session
        WHEN it is converted to a Practice model
        THEN it is converted correctly
        """
        complete_json = {
            "goals": [{"name": A_GOAL}],
            "exercises": [
                {
                    "name": AN_EXERCISE,
                    "bpm_start": A_BPM,
                    "bpm_end": A_BPM,
                    "minutes": SOME_MINUTES,
                },
                {
                    "name": OTHER_EXERCISE,
                    "bpm_start": A_BPM,
                    "bpm_end": A_BPM,
                    "minutes": SOME_MINUTES,
                },
            ],
            "positives": [{"name": A_POSITIVE}],
            "improvements": [{"name": AN_IMPROVEMENT}],
            "notes": A_NOTE,
        }
        model_expected = PracticeDTO(
            goals=[Goal(name=A_GOAL.lower())],
            improvements=[Improvement(name=AN_IMPROVEMENT.lower())],
            exercises=[
                Exercise(
                    name=OTHER_EXERCISE.lower(),
                    bpm_start=A_BPM,
                    bpm_end=A_BPM,
                    minutes=SOME_MINUTES,
                ),
                Exercise(
                    name=AN_EXERCISE.lower(),
                    bpm_start=A_BPM,
                    bpm_end=A_BPM,
                    minutes=SOME_MINUTES,
                ),
            ],
            positives=[Positive(name=A_POSITIVE.lower())],
            notes=A_NOTE,
        )

        model = PracticeDTO.json_to_model(complete_json)

        self.assertEqual(model_expected, model)

    def test_json_to_model_partial(self):
        """
        GIVEN a partial json object for a practice session
        WHEN it is converted to a Practice model
        THEN it fields holding partial data are not in the model
        """
        partial_json = {
            "goals": [{"name": ""}],
            "exercises": [
                {
                    "name": "",
                    "bpm_start": A_BPM,
                    "bpm_end": A_BPM,
                    "minutes": SOME_MINUTES,
                },
                {
                    "name": AN_EXERCISE,
                    "bpm_start": "",
                    "bpm_end": A_BPM,
                    "minutes": SOME_MINUTES,
                },
                {
                    "name": AN_EXERCISE,
                    "bpm_start": A_BPM,
                    "bpm_end": "",
                    "minutes": SOME_MINUTES,
                },
                {
                    "name": OTHER_EXERCISE,
                    "bpm_start": A_BPM,
                    "bpm_end": A_BPM,
                    "minutes": "",
                },
            ],
            "positives": [{"name": ""}],
            "improvements": [{"name": ""}],
            "notes": "",
        }
        model_expected = PracticeDTO(
            goals=[], exercises=[], positives=[], improvements=[], notes=None
        )

        model = PracticeDTO.json_to_model(partial_json)

        self.assertEqual(model_expected, model)

    def test_model_to_jsonable(self):
        """
        GIVEN a practice model
        WHEN it is coverted to a jsonable object
        THEN return a jsonable object
        """
        toast = "A very nice message ^^"
        exercises = [
            Exercise(
                name=AN_EXERCISE, bpm_start=A_BPM, bpm_end=A_BPM, minutes=SOME_MINUTES
            ),
            Exercise(
                name=OTHER_EXERCISE,
                bpm_start=A_BPM,
                bpm_end=A_BPM,
                minutes=SOME_MINUTES,
            ),
        ]
        model = create_complete_practice(
            self.a_profile,
            exercises=exercises,
            instrument=Instrument(name="piano"),
            goals=[Goal(name=A_GOAL)],
            improvements=[Improvement(name=AN_IMPROVEMENT)],
            positives=[Positive(name=A_POSITIVE)],
            notes="notes",
            date=timezone.now(),
        )

        jsonable = PracticeDTO.model_to_jsonable(model, toast)

        obj_expected = {
            "goals": [A_GOAL],
            "improvements": [AN_IMPROVEMENT],
            "positives": [A_POSITIVE],
            "notes": "notes",
            "exercises": [
                {
                    "name": AN_EXERCISE,
                    "bpm_start": A_BPM,
                    "bpm_end": A_BPM,
                    "minutes": SOME_MINUTES,
                },
                {
                    "name": OTHER_EXERCISE,
                    "bpm_start": A_BPM,
                    "bpm_end": A_BPM,
                    "minutes": SOME_MINUTES,
                },
            ],
            "toast": toast,
        }
        self.assertEqual(obj_expected, jsonable)
