import os
from datetime import timedelta
from unittest import mock

from django.utils import timezone
from django.test import TestCase

from musicavis.settings import EXPORTS_DIR
from app.models.practice import Instrument, Exercise
from app.models.user import Profile
from app.models.email_preferences import EmailPreferences
from app.models.notification import Notification
from app.backend.utils.enums import FileType, NewLine
from app.backend.dashboard.stats import PracticeStats
from app.tests.conftest import (create_user, create_user_with_a_practice, add_instruments_to_database,
                                create_task, create_complete_practice, A_USERNAME, OTHER_USERNAME, A_PASSWORD,
                                OTHER_PASSWORD, AN_EMAIL, OTHER_EMAIL, AN_INSTRUMENT, JobMock)

instruments = ['Cello', 'Violin']
instrument1 = Instrument(name=instruments[0])
instrument2 = Instrument(name=instruments[1])
exercises1 = [Exercise(name='C', bpm_start=80, bpm_end=75, minutes=40),
              Exercise(name='D', bpm_start=80, bpm_end=75, minutes=20)]
exercises2 = [Exercise(name='E', bpm_start=80, bpm_end=75, minutes=50),
              Exercise(name='F', bpm_start=80, bpm_end=75, minutes=20)]
exercises3 = [Exercise(name='G', bpm_start=80, bpm_end=75, minutes=40),
              Exercise(name='H', bpm_start=80, bpm_end=75, minutes=60)]


class UserModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        User.objects.all().delete()
        cls.a_user = create_user()
        cls.a_user_with_a_practice = create_user_with_a_practice()

    @classmethod
    def tearDownClass(cls):
        files = [f for f in os.listdir(EXPORTS_DIR)]
        for f in files:
            os.remove(f'{EXPORTS_DIR}/{f}')

    """
    GENERAL
    """

    def test_attributes_are_lowercase(self):
        """
        WHEN a user is created
        THEN it's name should be lowercase so that agent and Agent are the same user
        """
        user = create_user(A_USERNAME.upper(), AN_EMAIL, A_PASSWORD)

        self.assertTrue(user.username.islower())

    def test_attributes_are_lowercase(self):
        """
        WHEN a user is created
        THEN it's email should be lowercase
        """
        user = create_user(A_USERNAME + 'a', AN_EMAIL.upper(), A_PASSWORD)

        self.assertTrue(user.email.islower())

    def test_password_hashing(self):
        """
        WHEN a user's password is set
        THEN the password is hashed
        """
        self.assertTrue(self.a_user.verify_password(A_PASSWORD))
        self.assertFalse(self.a_user.verify_password(A_PASSWORD + '1234'))

    def test_salts_are_random(self):
        """
        WHEN two users register with the same password
        THEN the salts are different
        """
        other_user = create_user('oh', OTHER_EMAIL, A_PASSWORD)

        self.assertNotEqual(self.a_user.password, other_user.password)

    def test_update_email_preferences(self):
        """
        WHEN a user updates its email preferences
        THEN the email preferences are updated
        """
        before_features = self.a_user.email_preferences.features
        before_practicing = self.a_user.email_preferences.practicing
        before_promotions = self.a_user.email_preferences.promotions

        self.a_user.update_email_preferences(accept_features=(not before_features),
                                             accept_practicing=(not before_practicing),
                                             accept_promotions=(not before_promotions))

        self.assertEqual(self.a_user.email_preferences.features, not before_features)
        self.assertEqual(self.a_user.email_preferences.practicing, not before_practicing)
        self.assertEqual(self.a_user.email_preferences.promotions, not before_promotions)

    def test_stringify_models(self):
        """
        WHEN the models related to User are stringified
        THEN the stringified models are as expected
        """
        models = [(self.a_user, self.a_user.username),
                  (EmailPreferences(features=1, practicing=1, promotions=1), '[1,1,1]')]

        for model, expected_string in models:
            self.assertEqual(str(model), expected_string)

    def test_gravatar(self):
        """
        WHEN a user's gravatar url is assembled
        THEN the url generated is correct
        """
        actual_digest = self.a_user.avatar(128)

        self.assertEqual(
            actual_digest, 'https://www.gravatar.com/avatar/1aedb8d9dc4751e229a335e371db8058?d=identicon&s=128'
        )

    """
    PRACTICE
    """

    def test_add_new_practice_session(self):
        """
        WHEN a practice session is created
        THEN add the new session to the user's list of practices
        """
        npractices_before = len(self.a_user.practices.all())

        self.a_user.new_practice(AN_INSTRUMENT)
        self.a_user.new_practice(AN_INSTRUMENT)

        self.assertEqual(len(self.a_user.practices.all()), npractices_before + 2)

    def test_add_new_practice_session_instrument_field(self):
        """
        WHEN a practice session is created
        THEN ensure the correct instrument is tied to the session
        """
        instrument = Instrument.objects.filter(name=AN_INSTRUMENT).first()
        practice = User.objects.filter(username=self.a_user_with_a_practice.username).first().practices.all()[0]

        self.assertEqual(practice.instrument_id, instrument.id)

    def test_delete_practice_session_good_user(self):
        """
        WHEN the practice session is deleted
        THEN ensure it is deleted in the database
        """
        self.assertEqual(len(self.a_user_with_a_practice.practices.all()), 1)

        a_practice = self.a_user_with_a_practice.practices.all()[0]
        self.a_user_with_a_practice.delete_practice(a_practice)

        self.assertEqual(len(self.a_user_with_a_practice.practices.all()), 0)

    def test_delete_practice_session_bad_user(self):
        """
        GIVEN two users each with a practice session
        WHEN a user attempts to delete the other user's practice
        THEN do not delete the other user's practice session
        """
        self.a_user.new_practice(AN_INSTRUMENT)

        self.a_user.delete_practice(self.a_user_with_a_practice.practices.all()[0])

        self.assertEqual(len(self.a_user.practices.all()), 1)
        self.assertEqual(len(self.a_user_with_a_practice.practices.all()), 1)

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
    '''
    def test_valid_token(a_user):
        """
        WHEN a user changes his or her password with a valid token
        THEN the new password is set
        """
        token = a_user.generate_token(TokenType.RESET)
        is_password_changed = User.reset_password(token, OTHER_PASSWORD)

        assert is_password_changed
        assert a_user.verify_password(OTHER_PASSWORD)


    def test_expired_token(a_user):
        """
        WHEN a user changes his or her password with an invalid token
        THEN the password remains the same
        """
        token = a_user.generate_token(TokenType.RESET, 0.5)
        time.sleep(1)
        is_password_changed = User.reset_password(token, OTHER_PASSWORD)

        assert not is_password_changed
        assert not a_user.verify_password(OTHER_PASSWORD)


    def test_invalid_token(a_user):
        """
        GIVEN an invalid password reset token
        WHEN resetting the user's password
        THEN the second user's password remains the same
        """
        token = a_user.generate_token(TokenType.RESET) + 'a'

        is_password_changed = a_user.reset_password(token, OTHER_PASSWORD)

        assert not is_password_changed
        assert not a_user.verify_password(OTHER_PASSWORD)


    def test_confirm_account_valid_token(a_user):
        """
        GIVEN a confirmation token
        WHEN the user confirms the account
        THEN the account is confirmed
        """
        token = a_user.generate_token(TokenType.CONFIRM, A_WEEK)

        is_account_confirmed = a_user.confirm(token)

        assert is_account_confirmed


    def test_confirm_account_invalid_token(a_user, other_user):
        """
        GIVEN an invalid confirmation token
        AND another user
        WHEN the user confirms the account with the other user's token
        THEN the account is not confirmed
        """
        other_token = other_user.generate_token(TokenType.CONFIRM, A_WEEK)

        is_account_confirmed = a_user.confirm(other_token)

        assert not is_account_confirmed
    '''

    """
    PAGINATION
    """
    '''
    def test_paginate_practices(a_user_with_4_practices):
        """
        GIVEN a user with 4 exercises each 1 day apart
        WHEN the exercises are fetched, 3 exercises/page
        THEN they are listed in descending order
        """
        num_practices_per_page = 3
        practices = a_user_with_4_practices.paginate_practices(1, num_practices_per_page)

        assert num_practices_per_page == len(practices.items)
        assert practices.items[0].date > practices.items[-1].date


    def test_paginate_practices_last_page(a_user_with_4_practices):
        """
        GIVEN a user with 4 exercises each 1 day apart
        WHEN the second page of exercises is fetched
        THEN there is one practice in the list
        """
        num_practices_per_page = 3
        practices = a_user_with_4_practices.paginate_practices(2, num_practices_per_page)

        assert len(practices.items) == 1
    '''
    """
    EXPORTS
    """

    def test_export_practices(self):
        """
        WHEN the user exports his practices in every file type
        THEN return a file for every file type
        """
        username = self.a_user_with_a_practice.username
        fnames_expected = [f'{username}_practices_{timezone.now():%d%m%y}.{x.value}' for x in FileType]

        fnames = [self.a_user_with_a_practice.export_practices(NewLine.UNIX, x) for x in FileType]

        self.assertTrue(all([x == y for x, y in zip(fnames_expected, fnames)]))

    def test_get_practice_stats_has_practices(self):
        """
        GIVEN a user with at least 1 practice
        WHEN getting its practice stats
        THEN a PracticeStats object is returned
        """
        stats = self.a_user_with_a_practice.get_practice_stats()

        self.assertTrue(isinstance(stats, PracticeStats))

    def test_get_practice_stats_no_practice(self):
        """
        GIVEN a user has no practice
        WHEN getting its practice stats
        THEN nothing is returned
        """
        stats = self.a_user.get_practice_stats()

        self.assertIsNone(stats)

    def test_practice_time_to_dict(self):
        """
        GIVEN a user with three practices
        WHEN the creating a dict from the exercises
        THEN a dict with 'length' and 'date' fields is created
        """
        now = timezone.now()
        date1, date2 = now - timedelta(days=3), now - timedelta(days=1)
        practice1 = create_complete_practice(self.a_user, instrument1, date2, exercises1)
        practice2 = create_complete_practice(self.a_user, instrument2, now, exercises2)
        practice3 = create_complete_practice(self.a_user, instrument1, date1, exercises3)
        for practice in [practice1, practice2, practice3]:
            self.a_user.practices.add(practice)
        datasets_expected = {
            instruments[0]: [
                {'length': 100, 'date': f'{date1:%Y%m%d}'}, {'length': 0, 'date': f'{now - timedelta(days=2):%Y%m%d}'},
                {'length': 60, 'date': f'{date2:%Y%m%d}'}, {'length': 0, 'date': f'{now:%Y%m%d}'}
            ],
            instruments[1]: [
                {'length': 0, 'date': f'{date1:%Y%m%d}'}, {'length': 0, 'date': f'{now - timedelta(days=2):%Y%m%d}'},
                {'length': 0, 'date': f'{date2:%Y%m%d}'}, {'length': 70, 'date': f'{now:%Y%m%d}'}
            ]
        }
        dates_expected = [f'{date1:%Y%m%d}', f'{date1 + timedelta(days=1):%Y%m%d}', f'{date2:%Y%m%d}', f'{now:%Y%m%d}']

        data = self.a_user.practice_graph_data()

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
        self.a_user.add_notification('test', {'task_id': 1})

        self.assertEqual(len(Notification.objects.all()), 1)
        self.assertEqual(Notification.objects.all()[0].name, 'test')

    def test_add_notification_multiple(self):
        """
        WHEN two notifications of the same name are added to the user
        THEN only the latest one is associated with the user
        """
        self.a_user.add_notification('test', {'task_id': 1})
        self.a_user.add_notification('test', {'task_id': 2})

        self.assertEqual(len(Notification.objects.all()), 1)
        self.assertEqual(Notification.objects.all()[0].name, 'test')

    """
    TASKS
    """

    @mock.patch('app.models.user.export_practices')
    def test_launch_task_enqueue(self, mock_rq):
        """
        WHEN launching a task
        THEN the task is added to the task queue
        """
        mock_rq.delay.return_value = JobMock()

        self.a_user.launch_task('name', 'description')

        self.assertTrue(mock_rq.delay.called)

    def test_get_tasks_in_progress(self):
        """
        GIVEN two tasks in progress and one complete task in the database
        WHEN getting tasks in progress
        THEN return the tasks in progress
        """
        progress1 = create_task('ert', 'test1', 'testing1', self.a_user)
        progress2 = create_task('tre', 'test1', 'testing2', self.a_user)
        complete = create_task('tyu', 'test2', 'testing2', self.a_user, True)

        tasks = self.a_user.get_tasks_in_progress()

        self.assertEqual(len(tasks), 2)
        self.assertTrue(all([x in tasks for x in [progress1, progress2]]))

    def test_get_task_in_progress(self):
        """
        GIVEN two tasks in progress and one complete task in the database
        WHEN getting a task in progress
        THEN return the first task in progress
        """
        progress1 = create_task('ert', 'test1', 'testing1', self.a_user)
        progress2 = create_task('tre', 'test1', 'testing2', self.a_user)
        complete = create_task('tyu', 'test2', 'testing2', self.a_user, True)

        task = self.a_user.get_task_in_progress('test1')

        assert task == progress1
