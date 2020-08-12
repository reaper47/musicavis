from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from app.models.email_preferences import EmailPreferences
from app.tests.conftest import (
    create_user,
    A_USERNAME,
    AN_EMAIL,
    A_PASSWORD,
    OTHER_USERNAME,
    OTHER_EMAIL,
    OTHER_PASSWORD,
    is_user_index,
    is_login_form,
    is_signup_form,
    delete_users,
    is_password_reset_form,
    is_reset_password_form,
)
from app.tests.app.backend.auth.utils import (
    login_post,
    register_post,
    reset_post,
    reset_password_post,
)
from app.backend.utils.enums import TokenType

MOCK_EMAIL = "app.backend.auth.views.send_email_to_user"
MOCK_LOGOUT = "app.backend.auth.views.logout"


class AuthViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a_user = create_user()

    @classmethod
    def tearDownClass(cls):
        delete_users()

    """
    LOGIN TESTS
    """

    def test_login_form_displays(self):
        """
        WHEN the login page is rendered
        THEN display the components of the login form
        """
        response = self.client.get(reverse("app:auth.login"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_login_form(response))

    def test_login_correct_credentials(self):
        """
        WHEN a user logs in with the correct credentials
        THEN the user logs is successfully
        """
        credentials = {"username": A_USERNAME, "password": A_PASSWORD}
        self.client.login(**credentials)

        response = self.client.post(reverse("app:auth.login"), credentials, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_user_index(response))

    def test_login_incorrect_credentials(self):
        """
        WHEN a user logs in with incorrect credentials
        THEN the user is not logged in
        """
        response = login_post(self.client, A_USERNAME, "whoops!")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], reverse("app:auth.login"))

    def test_login_if_already_logged_in(self):
        """
        WHEN the user attempts to access the login page
        THEN do not render the login page
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)

        response = self.client.get(reverse("app:auth.login"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], reverse("app:main.index"))

    """
    SIGNUP TESTS
    """

    def test_register_form_displays(self):
        """
        WHEN one accesses the register page
        THEN the register form is displayed
        """
        response = self.client.get(reverse("app:auth.signup"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_signup_form(response))

    @mock.patch(MOCK_EMAIL)
    def test_register_new_user(self, mock_email):
        """
        WHEN one creates a new account
        THEN create a new account
        AND the user is logged in
        """
        response = register_post(
            self.client,
            OTHER_USERNAME,
            OTHER_EMAIL,
            A_PASSWORD,
            A_PASSWORD,
            send_emails=False,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_user_index(response))

    def test_register_disagree_terms(self):
        """
        WHEN a user does not agree to the terms of use
        THEN the user cannot register
        """
        response = register_post(
            self.client,
            OTHER_USERNAME,
            OTHER_EMAIL,
            A_PASSWORD,
            A_PASSWORD,
            agree_terms=False,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], reverse("app:auth.signup"))

    @mock.patch(MOCK_EMAIL)
    def test_register_disagree_emails(self, mock_email):
        """
        WHEN a user does not agree to receiving emails
        THEN the user's email preferences are all null
        """
        response = register_post(
            self.client,
            OTHER_USERNAME,
            "boo@ah.oops",
            A_PASSWORD,
            A_PASSWORD,
            send_emails=False,
        )

        user = User.objects.get(username=OTHER_USERNAME)
        email_preferences_expected = EmailPreferences(
            features=False, practicing=False, promotions=False
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.profile.email_preferences, email_preferences_expected)

    @mock.patch(MOCK_EMAIL)
    def test_register_new_user_send_confirmation_email(self, mock_email):
        """
        WHEN a new user registers
        THEN an account confirmation email is sent
        """
        response = register_post(
            self.client,
            OTHER_USERNAME,
            "boo@ah.oops",
            A_PASSWORD,
            A_PASSWORD,
            send_emails=False,
        )

        self.assertTrue(mock_email.called)
        self.assertIn(b"account confirmation", response.content)

    def test_register_if_already_logged_in(self):
        """
        WHEN the user attempts to access the register page
        THEN the user is redirected
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)

        response = self.client.get(reverse("app:auth.signup"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("app:main.index"))

    """
    LOGOUT TESTS
    """

    @mock.patch(MOCK_LOGOUT)
    def test_logout(self, mock_logout):
        """
        WHEN the user logouts
        THEN the user is logged out
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)

        response = self.client.get(reverse("app:auth.logout"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You have been logged out", response.content)
        self.assertTrue(mock_logout.called)

    """
    PASSWORD RESET TESTS
    """

    def test_password_reset_form_displays(self):
        """
        WHEN an anonymous user requests the password reset form
        THEN display the password reset form
        """
        response = self.client.get(reverse("app:auth.request_password_reset"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_password_reset_form(response))

    def test_password_reset_form_does_not_display_for_users(self):
        """
        WHEN a user accesses the password reset form
        THEN the user is redirected to the index page
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)

        response = self.client.get(reverse("app:auth.request_password_reset"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("app:main.index"))

    @mock.patch(MOCK_EMAIL)
    def test_password_reset_request_send_token(self, mock_email):
        """
        WHEN an anonymous user submits the password reset form
        THEN a reset token is sent by email
        """
        response = reset_post(self.client, AN_EMAIL)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_email.called)
        self.assertIn(b"an email with instructions", response.content.lower())

    @mock.patch(MOCK_EMAIL)
    def test_password_reset_request_go_to_login(self, mock_email):
        """
        WHEN a reset request is sent to an email not in the database
        THEN the user is redirected to the login page
        """
        response = reset_post(self.client, AN_EMAIL + "nonexistant")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(mock_email.called)
        self.assertTrue(is_login_form(response))

    def test_reset_password_form_displays(self):
        """
        GIVEN a valid password reset token for an anonymous user
        WHEN the anonymous clicks the token
        THEN the reset password form displays
        """
        token = self.a_user.profile.generate_token(TokenType.RESET)

        response = self.client.get(
            reverse("app:auth.password_reset", args=[token]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_reset_password_form(response))

    def test_reset_password_valid_token(self):
        """
        GIVEN a password reset form for an anonymous user
        WHEN the user submits the form
        THEN the user's password is updated
        AND is redirected to the login page
        """
        token = self.a_user.profile.generate_token(TokenType.RESET)

        response = reset_password_post(
            self.client, token, OTHER_PASSWORD, OTHER_PASSWORD, False
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("app:auth.login"))

    def test_reset_password_invalid_token(self):
        """
        GIVEN an invalid token
        WHEN the user submits the reset password form
        THEN the user is redirected to the index page
        """
        token = self.a_user.profile.generate_token(TokenType.RESET, 1)

        response = reset_password_post(
            self.client, token + "a", OTHER_PASSWORD, OTHER_PASSWORD, False
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("app:main.index"))

    def test_reset_password_already_logged_in(self):
        """
        WHEN the user accesses reset page with a token
        THEN the user is redirected to the index
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        token = self.a_user.profile.generate_token(TokenType.RESET)

        response = self.client.get(reverse("app:auth.password_reset", args=[token]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("app:main.index"))

    """
    CONFIRMATION EMAIL
    """

    @mock.patch(MOCK_EMAIL)
    def test_confirm_account_message_after_confirmation(self, mock_email):
        """
        GIVEN a user has not confirmed the account
        WHEN the user clicks the account confirmation link
        THEN the message asking to confirm the account disappeared
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        token = self.a_user.profile.generate_token(TokenType.CONFIRM)

        response = self.client.get(
            reverse("app:auth.confirm", args=[token]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"not confirmed", response.content)

    @mock.patch(MOCK_EMAIL)
    def test_confirm_account_send_welcome_email(self, mock_email):
        """
        GIVEN a user has not confirmed the account
        WHEN the user clicks the account confirmation link
        THEN a welcome email is sent to the user
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        token = self.a_user.profile.generate_token(TokenType.CONFIRM)

        self.client.get(reverse("app:auth.confirm", args=[token]))

        self.assertTrue(mock_email.called)

    @mock.patch(MOCK_EMAIL)
    def test_confirm_account_already_confirmed(self, mock_email):
        """
        GIVEN a user has already confirmed the account
        WHEN the user accesses the confirm url with a token
        THEN redirect to the index page
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        token = self.a_user.profile.generate_token(TokenType.CONFIRM)
        self.client.get(reverse("app:auth.confirm", args=[token]), follow=True)

        response = self.client.get(reverse("app:auth.confirm", args=[token]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("app:main.index"))

    def test_confirm_invalid_token(self):
        """
        GIVEN an invalid account confirmation token
        WHEN the user attempts to confirm the account
        THEN the account is not confirmed
        AND the user is redirected to the index page
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        token = self.a_user.profile.generate_token(TokenType.CONFIRM) + "a"

        response = self.client.get(
            reverse("app:auth.confirm", args=[token]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"link is invalid", response.content)

    @mock.patch(MOCK_EMAIL)
    def test_resend_confirm_account(self, mock_email):
        """
        GIVEN a signed-in user whose account is unconfirmed
        WHEN the user accesses the index page to request a confirmation email
        THEN an email is sent
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        token = self.a_user.profile.generate_token(TokenType.CONFIRM)

        response = self.client.get(
            reverse("app:auth.resend_confirm", args=[token]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_email.called)
        self.assertIn(b"new account confirmation", response.content)

    @mock.patch(MOCK_EMAIL)
    def test_resend_confirm_already_confirmed(self, mock_email):
        """
        GIVEN a user confirmed its account
        WHEN the user requests a new confirmation link
        THEN do not send an email
        AND flash the account is already confirmed
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        token = self.a_user.profile.generate_token(TokenType.CONFIRM)
        self.client.get(reverse("app:auth.confirm", args=[token]))
        mock_email.called = False

        response = self.client.get(
            reverse("app:auth.resend_confirm", args=[token]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(mock_email.called)
        self.assertIn(b"already confirmed", response.content)

    @mock.patch(MOCK_EMAIL)
    def test_resend_confirm_invalid_token(self, mock_email):
        """
        WHEN the user requests a new confirmation link with an invalid token
        THEN do not send an email
        AND flash the link is invalid
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        token = self.a_user.profile.generate_token(TokenType.CONFIRM) + "a"

        response = self.client.get(
            reverse("app:auth.resend_confirm", args=[token]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(mock_email.called)
        self.assertIn(b"link is invalid", response.content)

    """
    CONFIRMATION EMAIL
    """

    def test_unsubscribe_valid_token(self):
        """
        WHEN the clicks the unsubscribe link in an email
        THEN the user is unsubscribed from future emails
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        token = self.a_user.profile.generate_token(TokenType.UNSUBSCRIBE)

        response = self.client.get(
            reverse("app:auth.unsubscribe", args=[token]), follow=True
        )

        self.a_user.refresh_from_db()
        preferences_expected = EmailPreferences(
            features=False, promotions=False, practicing=False
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.a_user.profile.email_preferences, preferences_expected)

    def test_unsubscribe_invalid_token(self):
        """
        WHEN the unsubscribe token is bad
        THEN a unsubscribed failure message is displayed.
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        token = self.a_user.profile.generate_token(TokenType.UNSUBSCRIBE) + "a"

        response = self.client.get(
            reverse("app:auth.unsubscribe", args=[token]), follow=True
        )

        self.a_user.refresh_from_db()
        preferences_expected = EmailPreferences(
            features=False, promotions=False, practicing=False
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"link is invalid", response.content)
        self.assertNotEqual(self.a_user.profile.email_preferences, preferences_expected)
