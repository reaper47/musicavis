from unittest import mock

from django.test import TestCase

from app.backend.profile.utils import update_email
from app.tests.conftest import create_user, delete_users

MOCK_SEND_EMAIL = "app.backend.profile.utils.send_email_to_user"


class ProfileUtilsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a_user = create_user()

    @classmethod
    def tearDownClass(cls):
        delete_users()

    @mock.patch(MOCK_SEND_EMAIL)
    def test_update_email(self, mock_send_email):
        """
        WHEN a user's email is updated
        THEN the user is no longer confirmed
        AND a confirmation email is sent
        """
        update_email(self.a_user, "new@email.com")

        self.assertFalse(self.a_user.profile.is_confirmed)
        self.assertTrue(mock_send_email.called)
