import os
import time
from datetime import timedelta
from unittest import mock

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User

from musicavis.settings import EXPORTS_DIR
from app.models.practice import Instrument, Exercise, Goal, Improvement, Positive
from app.models.profile import Profile
from app.models.email_preferences import EmailPreferences
from app.models.notification import Notification
from app.backend.utils.enums import FileType, NewLine, TokenType
from app.backend.dashboard.stats import PracticeStats
from app.tests.conftest import (
    create_user,
    create_user_with_a_practice,
    add_instruments_to_database,
    create_task,
    create_complete_practice,
    A_USERNAME,
    A_PASSWORD,
    OTHER_PASSWORD,
    AN_EMAIL,
    OTHER_EMAIL,
    AN_INSTRUMENT,
    JobMock,
    delete_users,
)

instruments = ["Cello", "Violin"]
instrument1 = Instrument(name=instruments[0])
instrument2 = Instrument(name=instruments[1])
exercises1 = [
    Exercise(name="C", bpm_start=80, bpm_end=75, minutes=40),
    Exercise(name="D", bpm_start=80, bpm_end=75, minutes=20),
]
exercises2 = [
    Exercise(name="E", bpm_start=80, bpm_end=75, minutes=50),
    Exercise(name="F", bpm_start=80, bpm_end=75, minutes=20),
]
exercises3 = [
    Exercise(name="G", bpm_start=80, bpm_end=75, minutes=40),
    Exercise(name="H", bpm_start=80, bpm_end=75, minutes=60),
]

A_WEEK = 604800  # in seconds


class ProfileModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a_user = create_user()
        cls.a_user_with_a_practice = create_user_with_a_practice()

    @classmethod
    def tearDownClass(cls):
        files = [f for f in os.listdir(EXPORTS_DIR)]
        for f in files:
            os.remove(f"{EXPORTS_DIR}/{f}")
        delete_users()

    """
    GENERAL
    """

    def test_attributes_username_is_lowercase(self):
        """
        WHEN a user is created
        THEN it's name should be lowercase so that agent and Agent are the same user
        """
        self.assertTrue(self.a_user.username.islower())

    def test_attributes_email_is_lowercase(self):
        """
        WHEN a user is created
        THEN it's email should be lowercase
        """
        user = create_user(A_USERNAME + "a", AN_EMAIL.upper(), A_PASSWORD)

        self.assertTrue(user.email.islower())

    def test_password_hashing(self):
        """
        WHEN a user's password is set
        THEN the password is hashed
        """
        self.assertTrue(self.a_user.profile.verify_password(A_PASSWORD))
        self.assertFalse(self.a_user.profile.verify_password(A_PASSWORD + "1234"))

    def test_salts_are_random(self):
        """
        WHEN two users register with the same password
        THEN the salts are different
        """
        other_user = create_user("oh", OTHER_EMAIL, A_PASSWORD)

        self.assertNotEqual(self.a_user.password, other_user.password)

    def test_update_email_preferences(self):
        """
        WHEN a user updates its email preferences
        THEN the email preferences are updated
        """
        before_features = self.a_user.profile.email_preferences.features
        before_practicing = self.a_user.profile.email_preferences.practicing
        before_promotions = self.a_user.profile.email_preferences.promotions

        self.a_user.profile.update_email_preferences(
            accept_features=(not before_features),
            accept_practicing=(not before_practicing),
            accept_promotions=(not before_promotions),
        )

        self.a_user.profile.email_preferences.refresh_from_db()
        self.assertEqual(
            self.a_user.profile.email_preferences.features, not before_features
        )
        self.assertEqual(
            self.a_user.profile.email_preferences.practicing, not before_practicing
        )
        self.assertEqual(
            self.a_user.profile.email_preferences.promotions, not before_promotions
        )

    def test_stringify_models(self):
        """
        WHEN the models related to User are stringified
        THEN the stringified models are as expected
        """
        models = [
            (self.a_user, self.a_user.username),
            (EmailPreferences(features=1, practicing=1, promotions=1), "[1,1,1]"),
        ]

        for model, expected_string in models:
            self.assertEqual(str(model), expected_string)

    def test_gravatar(self):
        """
        WHEN a user's gravatar url is assembled
        THEN the url generated is correct
        """
        digest_actual = self.a_user.profile.avatar(128)

        digest_expected = ("https://www.gravatar.com/avatar/"
                           "b682f93ed660ecda33e9adb4e514aa2f?d=identicon&s=128")
        self.assertEqual(digest_actual, digest_expected)

    def test_html_list_instruments_practiced_many_instruments(self):
        """
        GIVEN three instrument practiced
        WHEN the instruments practiced are formatted as an HTML list
        THEN the list is formatted correctly
        """
        name1, name2, name3 = "red", "green", "blue"
        for name in [name1, name2, name3]:
            instrument = Instrument.objects.create(name=name)
            self.a_user.profile.instruments_practiced.add(instrument)
        format_expected = "- Red<br>- Green<br>- Blue"

        format_actual = self.a_user.profile.list_instruments_practiced_html()

        self.assertEqual(format_actual, format_expected)

    def test_html_list_instruments_practiced_no_instruments(self):
        """
        GIVEN no instruments practiced
        WHEN the instruments practiced are formatted as an HTML list
        THEN the list is formatted correctly
        """
        format_expected = "None"

        format_actual = self.a_user.profile.list_instruments_practiced_html()

        self.assertEqual(format_actual, format_expected)

    """
    PRACTICE
    """

    def test_new_practice_session(self):
        """
        WHEN a practice session is created
        THEN add the new session to the user's list of practices
        """
        npractices_before = self.a_user.profile.practices.count()

        self.a_user.profile.new_practice(AN_INSTRUMENT)
        self.a_user.profile.new_practice(AN_INSTRUMENT)

        self.assertEqual(self.a_user.profile.practices.count(), npractices_before + 2)

    def test_new_practice_session_instrument_field(self):
        """
        WHEN a practice session is created
        THEN ensure the correct instrument is tied to the session
        """
        instrument = Instrument.objects.filter(name=AN_INSTRUMENT).first()
        practice = self.a_user_with_a_practice.profile.practices.first()

        self.assertEqual(practice.instrument_id, instrument.id)

    def test_new_practice_session_copy_previous_session(self):
        """
        GIVEN a user with two practice sessions, each for a different instrument
        WHEN a practice session is created
        AND the user wants the previous session copied over for an instrument
        THEN the content of the previous session is copied correctly
        """
        instrument1.save()
        instrument2.save()
        self.a_user.profile.new_practice(instrument1)
        practice = self.a_user.profile.new_practice(instrument2)
        practice.goals.set([Goal.objects.create(name="Test")])
        practice.exercises.set(
            [Exercise.objects.create(name="C", bpm_start=80, bpm_end=75, minutes=40)]
        )
        practice.improvements.set([Improvement.objects.create(name="Improvement1")])
        practice.positives.set([Positive.objects.create(name="Positive1")])
        practice.notes = "some notes..."

        self.a_user.profile.new_practice(instrument2, True)
        practice_actual = self.a_user.profile.practices.filter(
            instrument=instrument2
        ).last()

        self.assertNotEqual(practice_actual.date, practice.date)
        self.assertEqual(list(practice_actual.goals.all()), list(practice.goals.all()))
        self.assertEqual(
            list(practice_actual.exercises.all()), list(practice.exercises.all())
        )
        self.assertListEqual(
            list(practice_actual.improvements.all()), list(practice.improvements.all())
        )
        self.assertListEqual(
            list(practice_actual.positives.all()), list(practice.positives.all())
        )
        self.assertEqual(practice.notes, practice.notes)

    def test_delete_practice_session_good_user(self):
        """
        WHEN the practice session is deleted
        THEN ensure it is deleted in the database
        """
        self.assertEqual(self.a_user_with_a_practice.profile.practices.count(), 1)

        a_practice = self.a_user_with_a_practice.profile.practices.all()[0]
        self.a_user_with_a_practice.profile.delete_practice(a_practice)

        self.assertEqual(self.a_user_with_a_practice.profile.practices.count(), 0)

    def test_delete_practice_session_bad_user(self):
        """
        GIVEN two users each with a practice session
        WHEN a user attempts to delete the other user's practice
        THEN do not delete the other user's practice session
        """
        self.a_user.profile.new_practice(AN_INSTRUMENT)

        self.a_user.profile.delete_practice(
            self.a_user_with_a_practice.profile.practices.all()[0]
        )

        self.assertEqual(self.a_user.profile.practices.count(), 1)
        self.assertEqual(self.a_user_with_a_practice.profile.practices.count(), 1)

    def test_instruments_practiced(self):
        """
        GIVEN a user sets the instruments he or she plays
        WHEN the user tweaks the instruments he or she plays
        THEN their instruments played list is updated correctly
        """
        add_instruments_to_database()
        instruments = list(Instrument.objects.all())
        self.a_user.instruments_practiced = instruments

        new_instruments = instruments[0]
        self.a_user.instruments_practiced = new_instruments

        self.assertEqual(self.a_user.instruments_practiced, new_instruments)

    """
    TOKENS
    """

    def test_valid_token(self):
        """
        WHEN a user changes his or her password with a valid token
        THEN the new password is set
        """
        token = self.a_user.profile.generate_token(TokenType.RESET)
        is_password_changed = Profile.reset_password(token, OTHER_PASSWORD)

        user = User.objects.get(pk=self.a_user.pk)
        self.assertTrue(is_password_changed)
        self.assertTrue(user.check_password(OTHER_PASSWORD))

    def test_expired_token(self):
        """
        WHEN a user changes his or her password with an invalid token
        THEN the password remains the same
        """
        token = self.a_user.profile.generate_token(TokenType.RESET, 0.5)
        time.sleep(1)
        is_password_changed = Profile.reset_password(token, OTHER_PASSWORD)

        user = User.objects.get(pk=self.a_user.pk)
        self.assertFalse(is_password_changed)
        self.assertFalse(user.check_password(OTHER_PASSWORD))

    def test_invalid_token(self):
        """
        GIVEN an invalid password reset token
        WHEN resetting the user's password
        THEN the second user's password remains the same
        """
        token = self.a_user.profile.generate_token(TokenType.RESET) + "a"

        is_password_changed = Profile.reset_password(token, OTHER_PASSWORD)

        user = User.objects.get(pk=self.a_user.pk)
        self.assertFalse(is_password_changed)
        self.assertFalse(user.check_password(OTHER_PASSWORD))

    def test_confirm_account_valid_token(self):
        """
        GIVEN a confirmation token
        WHEN the user confirms the account
        THEN the account is confirmed
        """
        token = self.a_user.profile.generate_token(TokenType.CONFIRM, A_WEEK)

        is_account_confirmed = self.a_user.profile.confirm(token)

        user = User.objects.get(pk=self.a_user.pk)
        self.assertTrue(is_account_confirmed)
        self.assertTrue(user.is_active)

    def test_confirm_account_invalid_token(self):
        """
        GIVEN an invalid confirmation token
        AND another user
        WHEN the user confirms the account with the other user's token
        THEN the account is not confirmed
        """
        other_user = create_user("Bob", OTHER_EMAIL, OTHER_PASSWORD)
        other_token = other_user.profile.generate_token(TokenType.CONFIRM, A_WEEK)

        is_account_confirmed = self.a_user.profile.confirm(other_token)

        user = User.objects.get(pk=self.a_user.pk)
        self.assertFalse(is_account_confirmed)
        self.assertTrue(user.is_active)

    """
    EXPORTS
    """

    def test_export_practices(self):
        """
        WHEN the user exports his practices in every file type
        THEN return a file for every file type
        """
        username = self.a_user_with_a_practice.username
        fnames_expected = [
            f"{username}_practices_{timezone.now():%d%m%y}.{x.value}" for x in FileType
        ]

        fnames = [
            self.a_user_with_a_practice.profile.export_practices(NewLine.UNIX, x)
            for x in FileType
        ]

        self.assertTrue(all([x == y for x, y in zip(fnames_expected, fnames)]))

    def test_get_practice_stats_has_practices(self):
        """
        GIVEN a user with at least 1 practice
        WHEN getting its practice stats
        THEN a PracticeStats object is returned
        """
        stats = self.a_user_with_a_practice.profile.get_practice_stats()

        self.assertIsInstance(stats, PracticeStats)

    def test_get_practice_stats_no_practice(self):
        """
        GIVEN a user has no practice
        WHEN getting its practice stats
        THEN nothing is returned
        """
        stats = self.a_user.profile.get_practice_stats()

        self.assertIsNone(stats)

    def test_practice_time_to_dict(self):
        """
        GIVEN a user with three practices
        WHEN the creating a dict from the exercises
        THEN a dict with 'length' and 'date' fields is created
        """
        now = timezone.now()
        date1, date2 = now - timedelta(days=3), now - timedelta(days=1)
        practice1 = create_complete_practice(
            self.a_user, instrument1, date2, exercises1
        )
        practice2 = create_complete_practice(self.a_user, instrument2, now, exercises2)
        practice3 = create_complete_practice(
            self.a_user, instrument1, date1, exercises3
        )
        for practice in [practice1, practice2, practice3]:
            self.a_user.profile.practices.add(practice)
        datasets_expected = {
            instruments[0]: [
                {"length": 100, "date": f"{date1:%Y%m%d}"},
                {"length": 0, "date": f"{now - timedelta(days=2):%Y%m%d}"},
                {"length": 60, "date": f"{date2:%Y%m%d}"},
                {"length": 0, "date": f"{now:%Y%m%d}"},
            ],
            instruments[1]: [
                {"length": 0, "date": f"{date1:%Y%m%d}"},
                {"length": 0, "date": f"{now - timedelta(days=2):%Y%m%d}"},
                {"length": 0, "date": f"{date2:%Y%m%d}"},
                {"length": 70, "date": f"{now:%Y%m%d}"},
            ],
        }
        dates_expected = [
            f"{date1:%Y%m%d}",
            f"{date1 + timedelta(days=1):%Y%m%d}",
            f"{date2:%Y%m%d}",
            f"{now:%Y%m%d}",
        ]

        data = self.a_user.profile.practice_graph_data()

        self.assertEqual(data.sets, datasets_expected)
        self.assertEqual(data.dates, dates_expected)

    """
    NOTIFICATIONS
    """

    def test_add_notification(self):
        """
        WHEN a notification is added to the user
        THEN a notification of the same name is added to the database
        """
        self.a_user.profile.add_notification("test", {"task_id": 1})

        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.all()[0].name, "test")

    def test_add_notification_multiple(self):
        """
        WHEN two notifications of the same name are added to the user
        THEN only the latest one is associated with the user
        """
        self.a_user.profile.add_notification("test", {"task_id": 1})
        self.a_user.profile.add_notification("test", {"task_id": 2})

        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.all()[0].name, "test")

    """
    TASKS
    """

    @mock.patch("app.models.profile.export_practices")
    def test_launch_task_enqueue(self, mock_rq):
        """
        WHEN launching a task
        THEN the task is added to the task queue
        """
        mock_rq.delay.return_value = JobMock()

        self.a_user.profile.launch_task(
            "name", "description", os="linux", file_type="pdf"
        )

        self.assertTrue(mock_rq.delay.called)

    def test_get_tasks_in_progress(self):
        """
        GIVEN two tasks in progress and one complete task in the database
        WHEN getting tasks in progress
        THEN return the tasks in progress
        """
        progress1 = create_task("ert", "test1", "testing1", self.a_user.profile)
        progress2 = create_task("tre", "test1", "testing2", self.a_user.profile)

        tasks = self.a_user.profile.get_tasks_in_progress()

        self.assertEqual(len(tasks), 2)
        self.assertTrue(all([x in tasks for x in [progress1, progress2]]))

    def test_get_task_in_progress(self):
        """
        GIVEN two tasks in progress and one complete task in the database
        WHEN getting a task in progress
        THEN return the first task in progress
        """
        progress1 = create_task("ert", "test1", "testing1", self.a_user.profile)
        progress2 = create_task("tre", "test1", "testing2", self.a_user.profile)  # noqa

        task = self.a_user.profile.get_task_in_progress("test1")

        self.assertEqual(task, progress1)
