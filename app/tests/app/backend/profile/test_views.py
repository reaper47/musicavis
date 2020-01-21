from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from app.models.practice import Instrument
from app.backend.utils.instruments import populate_db
from .utils import change_email, change_password, change_username
from app.tests.conftest import (create_user, delete_users, A_USERNAME, A_PASSWORD, OTHER_PASSWORD, OTHER_PASSWORD,
                                OTHER_EMAIL, is_profile_page, is_settings_page, is_access_settings, AN_EMAIL,
                                OTHER_USERNAME, is_practice_settings_page, SOME_INSTRUMENTS)

MOCK_UPDATE_EMAIL = 'app.backend.profile.views.update_email'


class ProfileViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a_user = create_user()

        cls.url_profile = reverse('app:profile.profile')
        cls.url_export_practices = reverse('app:profile.export_practices')
        cls.url_settings = reverse('app:profile.settings')
        cls.url_settings_access = reverse('app:profile.settings_access')
        cls.url_settings_practice = reverse('app:profile.settings_practice')
        cls.url_settings_profile = reverse('app:profile.settings_profile')
        cls.url_add_instrument = reverse('app:profile.add_new_instrument')
        cls.url_delete_account = reverse('app:profile.delete_account')
        cls.url_practice_new = reverse('app:practice.new')

        populate_db()

    @classmethod
    def tearDownClass(cls):
        delete_users()
        Instrument.objects.all().delete()

    def setUp(self):
        self.client.login(username=A_USERNAME, password=A_PASSWORD)

    def test_require_being_logged_in(self):
        """
        GIVEN a list of all endpoints for the profile blueprint
        WHEN an anonymous user accesses any of the settings and profile endpoints
        THEN the user is redirected to the login page
        """
        self.client.logout()
        endpoints = [
            self.url_profile, self.url_settings, self.url_settings_access,
            self.url_settings_practice, self.url_settings_profile
        ]

        responses = [self.client.get(x) for x in endpoints]

        url_login = reverse('app:auth.login')
        for response in responses:
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url[:7], url_login)

    def test_profile_page(self):
        """
        WHEN a user accesses the profile page
        THEN the profile page is displayed
        """
        response = self.client.get(self.url_profile, follow=True)

        self.assertTrue(is_profile_page(response))

    """
    SETTINGS TESTS
    """

    def test_render_settings_page(self):
        """
        WHEN a user accesses the settings page
        THEN the settings are displayed
        """
        response = self.client.get(self.url_settings, follow=True)

        self.assertTrue(is_settings_page(response))

    """
    SETTINGS ACCESS TESTS
    """

    def test_render_access_page(self):
        """
        WHEN a user accesses the Access settings
        THEN the forms for changing the password, email and username are displayed
        """
        response = self.client.get(self.url_settings_access, follow=True)

        self.assertTrue(is_access_settings(response))

    def test_update_password(self):
        """
        WHEN a user updates the password
        THEN the password is updated
        """
        response = change_password(self.client, A_PASSWORD, OTHER_PASSWORD, OTHER_PASSWORD)
        self.a_user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.a_user.profile.verify_password(OTHER_PASSWORD))

    def test_update_password_fails_when_incorrect_password(self):
        """
        WHEN the user changes the password but the current password is incorrect
        THEN the current password remains unchanged
        """
        self.a_user.profile.update_password(A_PASSWORD)

        response = change_password(self.client, OTHER_PASSWORD, OTHER_PASSWORD, OTHER_PASSWORD)
        self.a_user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.a_user.profile.verify_password(OTHER_PASSWORD))

    @mock.patch(MOCK_UPDATE_EMAIL)
    def test_update_email(self, mock_update_email):
        """
        WHEN a user updates the email address with a valid email address
        THEN the email address is updated
        AND the account is no longer confirmed
        AND a confirmation link is sent
        """
        response = change_email(self.client, OTHER_EMAIL, OTHER_EMAIL, A_PASSWORD)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(mock_update_email.called)

    def test_update_email_wrong_password(self):
        """
        WHEN the user changes his email but made a typo in his password
        THEN the email is not changed
        """
        response = change_email(self.client, OTHER_EMAIL, OTHER_EMAIL, OTHER_PASSWORD)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.a_user.email, AN_EMAIL)

    def test_update_username(self):
        """
        WHEN a user updates the username with a valid name
        THEN the username is updated
        """
        old_username = self.a_user.username

        response = change_username(self.client, OTHER_USERNAME, A_PASSWORD)

        self.assertEqual(response.status_code, 302)
        self.assertIsNone(User.objects.filter(username=old_username).first())

    def test_update_username_incorrect_password(self):
        """
        WHEN a user changes his username but made a typo in his password
        THEN do not update the username
        """
        old_username = self.a_user.username

        response = change_username(self.client, OTHER_USERNAME, OTHER_PASSWORD)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.a_user.username, old_username)

    """
    SETTINGS PRACTICE TESTS
    """

    def test_render_practice_settings_page(self):
        """
        WHEN the practice settings page is requested
        THEN render the page
        """
        response = self.client.get(self.url_settings_practice, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_practice_settings_page(response))

    def test_select_instruments_played(self):
        """
        GIVEN a user selects multiple instruments played
        WHEN the profile settings page is accessed
        THEN all instruments played are displayed in the instruments area
        """
        selected_instruments = [x.lower() for x in SOME_INSTRUMENTS]
        self.client.post(self.url_settings_practice,
                         data=dict(instruments=selected_instruments),
                         follow=True)

        response = self.client.get(self.url_profile)

        self.assertEqual(response.status_code, 200)
        text = response.content.decode().lower()
        self.assertTrue(all([x in text for x in selected_instruments]))

    def test_select_instruments_practiced_new_practice_single_instrument(self):
        """
        GIVEN a user has selected 1 default instrument
        WHEN a new practice is requested
        THEN the instrument selection screen is skipped
        """
        self.a_user.profile.update_instruments_practiced([Instrument.objects.all().first()])

        response = self.client.get(self.url_practice_new, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'New Practice Session', response.content)

    def test_select_instruments_practiced_new_practice_multiple_instrument(self):
        """
        GIVEN a user has selected multiple instruments
        WHEN a new practice is requested
        THEN the instrument selection screen is shown
        """
        self.a_user.profile.update_instruments_practiced(Instrument.objects.all()[:6])

        response = self.client.get(self.url_practice_new, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Practice Session', response.content)

    """
    SETTINGS PROFILE TESTS
    """
    '''
    def test_render_profile_settings_page(test_client, a_user_logged_in):
        """
        WHEN the profile settings page is requested
        THEN it the page is rendered
        """
        response = self.client.get('/settings/profile', follow=True)

        self.assertEqual(response.status_code, 200)
        assert is_profile_settings_page(response)


    @mock.patch(MOCK_CURRENT_USER)
    def test_email_preferences_select_none(mock_current_user, test_client, a_user_logged_in):
        """
        WHEN the user unchecks all of the email preferences
        THEN they are updated
        """
        response = test_client.post('/settings/profile',
                                    data=dict(practicing=False, promotions=False, features=False),
                                    follow=True)

        self.assertEqual(response.status_code, 200)
        assert mock_current_user.update_email_preferences.called


    """
    DELETE ACCOUNT
    """


    @mock.patch(MOCK_LOGOUT)
    def test_delete_account_ensure_user_logged_in(mock_logout, test_client):
        """
        WHEN the user requests his account to be deleted
        THEN ensure the user is logged in to prevent a cURL POST
        """
        _post_delete(test_client)

        assert not mock_logout.called


    @mock.patch(MOCK_LOGOUT)
    def test_delete_account_ensure_user_is_logged_out(mock_logout, test_client, a_user_logged_in):
        """
        WHEN a user deletes the account
        THEN the user is logged out
        """
        response = _post_delete(test_client)

        assert response.get_data(as_text=True)[-1] == '/'
        assert mock_logout.called


    def test_delete_account_account_deleted(test_client, a_user_logged_in):
        """
        WHEN the user requests his account to be deleted
        THEN the account is deleted
        """
        username = a_user_logged_in.username

        _post_delete(test_client)

        assert User.query.filter_by(username=username).first() is None


    def test_delete_account_identical_passwords(test_client, a_user_logged_in):
        """
        WHEN a user requests his account to be deleted with the wrong credentials
        THEN the account remains intact
        """
        _post_delete(test_client, is_wrong_password=True)

        assert User.query.filter_by(username=a_user_logged_in.username).first() is not None


    def test_delete_remove_email_preferences(test_client, a_user_logged_in):
        """
        WHEN a user deletes his account
        THEN the email preferences tied to the account are deleted
        """
        num_preferences = len(EmailPreferences.query.all())

        _post_delete(test_client)
        num_preferences_actual = len(EmailPreferences.query.all())

        assert num_preferences_actual == num_preferences - 1


    def test_delete_remove_practices(test_client, a_user_logged_in, a_user_with_4_practices):
        """
        GIVEN a user with 4 practices
        WHEN the user deletes his account
        THEN the practices tied to the account are deleted
        """
        num_practices = len(Practice.query.all())

        _post_delete(test_client)
        num_practices_actual = len(Practice.query.all())

        assert num_practices_actual == num_practices - 4


    def _post_delete(test_client, is_wrong_password=False):
        password = A_PASSWORD + 'a' if is_wrong_password else A_PASSWORD
        return test_client.post('/delete-account',
                                data=json.dumps(dict(password=password)),
                                content_type='application/json')


    """
    EXPORT PRACTICES
    """


    @mock.patch(MOCK_CURRENT_USER)
    def test_export_practices_task_not_in_progress(mock_current_user, test_client, a_user_logged_in):
        """
        WHEN the user requests to export the practices
        THEN a new task is launched
        """
        mock_current_user.get_task_in_progress.return_value = False
        mock_current_user.launch_task.return_value = None

        response = test_client.post('/export_practices', data=dict(file_type='pdf'),
                                    environ_base={'HTTP_USER_AGENT': 'linux'})

        assert response.data == b''
        assert mock_current_user.launch_task.called


    @mock.patch(MOCK_CURRENT_USER)
    def test_export_practices_task_in_progress(mock_current_user, test_client, a_user_logged_in):
        """
        WHEN the user requests to export the practices
        THEN a new task is launched
        """
        mock_current_user.get_task_in_progress.return_value = True

        response = test_client.post('/export_practices', data=dict(file_type='pdf'))

        assert response.data == b'task in progress'


    """
    ADD NEW INSTRUMENT
    """


    def test_add_new_instrument_empty_string(test_client, a_user_logged_in):
        """
        GIVEN an empty instrument name
        WHEN adding a new instrument to the database
        THEN the instrument is not added
        """
        instruments_before = Instrument.query.all()

        response = test_client.post('/add-new-instrument', query_string=dict(name=''))

        assert int(response.get_data(as_text=True)) == 400
        assert instruments_before == Instrument.query.all()


    def test_add_new_instrument_non_empty_string(test_client, a_user_logged_in):
        """
        GIVEN an instrument name
        WHEN adding a new instrument to the database
        THEN the instrument is added
        """
        instrument = Instrument(name='test')
        instrument_before = Instrument.query.filter_by(name=instrument.name).first()

        response = test_client.post('/add-new-instrument', query_string=dict(name=instrument.name))
        instrument_after = Instrument.query.filter_by(name=instrument.name).first()

        assert int(response.get_data(as_text=True)) == 200
        assert instrument_before is None
        assert instrument_after.name == instrument.name


    def test_add_new_instrument_already_exists(test_client, a_user_logged_in):
        """
        GIVEN an instrument name that is already in the database
        WHEN adding a new instrument to the database
        THEN the instrument is not added
        """
        instrument = Instrument(name='test')
        commit(instrument)
        instruments_before = Instrument.query.all()

        response = test_client.post('/add-new-instrument', query_string=dict(name=instrument.name))

        assert int(response.get_data(as_text=True)) == 400
        assert instruments_before == Instrument.query.all()
    '''
