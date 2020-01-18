from django.test import TestCase
from django.urls import reverse

from app.models.user import User
from app.tests.conftest import (create_user, A_USERNAME, A_PASSWORD, OTHER_USERNAME, OTHER_EMAIL,
                                is_user_index, is_login_form, is_signup_form)
from app.tests.app.backend.auth.utils import login_post, register_post


class AuthViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        User.objects.all().delete()
        cls.a_user = create_user()
        super(AuthViewsTests, cls).setUpClass()

    """
    LOGIN TESTS
    """

    def test_login_form_displays(self):
        """
        WHEN the login page is rendered
        THEN display the components of the login form
        """
        response = self.client.get(reverse('app:auth.login'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_login_form(response))

    def test_login_correct_credentials(self):
        """
        WHEN a user logs in with the correct credentials
        THEN the user logs is successfully
        """
        credentials = {'username': A_USERNAME, 'password': A_PASSWORD}
        self.client.login(**credentials)

        response = self.client.post(reverse('app:auth.login'), credentials, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_user_index(response))

    def test_login_incorrect_credentials(self):
        """
        WHEN a user logs in with incorrect credentials
        THEN the user is not logged in
        """
        response = login_post(self.client, A_USERNAME, 'whoops!')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('app:auth.login'))

    def test_login_if_already_logged_in(self):
        """
        WHEN the user attempts to access the login page
        THEN do not render the login page
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)

        response = self.client.get(reverse('app:auth.login'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('app:main.index'))

    """
    SIGNUP TESTS
    """

    def test_register_form_displays(self):
        """
        WHEN one accesses the register page
        THEN the register form is displayed
        """
        response = self.client.get(reverse('app:auth.signup'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_signup_form(response))

    def test_register_new_user(self):
        """
        WHEN one creates a new account
        THEN create a new account
        AND the user is logged in
        """
        response = register_post(self.client, OTHER_USERNAME, OTHER_EMAIL, A_PASSWORD, A_PASSWORD)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_user_index(response))

    def test_register_disagree_terms(self):
        """
        WHEN a user does not agree to the terms of use
        THEN the user cannot register
        """
        response = register_post(self.client, OTHER_USERNAME, OTHER_EMAIL, A_PASSWORD, A_PASSWORD, agree_terms=False)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('app:auth.signup'))

    '''
    def test_register_disagree_emails(test_client, init_database):
        """
        WHEN a user does not agree to receiving emails
        THEN the user's email preferences are all null
        """
        response = register(test_client, OTHER_USERNAME, OTHER_EMAIL, A_PASSWORD, A_PASSWORD, send_emails=False)

        user = User.query.filter_by(username=OTHER_USERNAME).first()
        assert response.status_code == 200
        assert user.email_preferences == EmailPreferences(False, False, False)


    @mock.patch(MOCK_CONFIRM_EMAIL)
    def test_register_new_user_send_confirmation_email(mock_email, test_client, init_database):
        """
        WHEN a new user registers
        THEN an account confirmation email is sent
        """
        response = register(test_client, OTHER_USERNAME, OTHER_EMAIL, A_PASSWORD, A_PASSWORD)

        assert mock_email.called
        assert b'account confirmation' in response.data


    def test_register_if_already_logged_in(test_client, a_user_logged_in):
        """
        WHEN the user attempts to access the register page
        THEN the user is redirected
        """
        response = test_client.get('/signup')

        assert response.status_code == 302
        assert is_index(response)


    """
    LOGOUT TESTS
    """


    def test_logout(test_client, a_user_logged_in):
        """
        WHEN the user logouts
        THEN the user is logged out
        """
        response = test_client.get('/logout', follow_redirects=True)

        assert response.status_code == 200
        assert b'You have been logged out' in response.data


    """
    PASSWORD RESET TESTS
    """


    def test_password_reset_form_displays(test_client):
        """
        WHEN an anonymous user requests the password reset form
        THEN display the password reset form
        """
        response = test_client.get('/reset', follow_redirects=True)

        assert response.status_code == 200
        assert is_reset_form(response)


    def test_password_reset_form_does_not_display_for_users(test_client, a_user_logged_in):
        """
        WHEN a user accesses the password reset form
        THEN the user is redirected to the index page
        """
        response = test_client.get('/reset')

        assert response.status_code == 302
        assert is_index(response)


    @mock.patch(MOCK_EMAIL)
    def test_password_reset_request_send_token(mock_email, test_client, init_database):
        """
        WHEN an anonymous user submits the password reset form
        THEN a reset token is sent by email
        """
        response = reset(test_client, AN_EMAIL)

        assert response.status_code == 200
        assert mock_email.called
        assert 'an email with instructions' in response.get_data(as_text=True).lower()


    @mock.patch(MOCK_EMAIL)
    def test_password_reset_request_go_to_login(mock_email, test_client, init_database):
        """
        WHEN a reset request is sent to an email not in the database
        THEN the user is redirected to the login page
        """
        response = reset(test_client, AN_EMAIL + 'nonexistant')

        assert response.status_code == 200
        assert not mock_email.called
        assert is_login_form(response)


    def test_reset_password_form_displays(test_client, init_database, a_user):
        """
        GIVEN a valid password reset token for an anonymous user
        WHEN the anonymous clicks the token
        THEN the reset password form displays
        """
        token = a_user.generate_token(TokenType.RESET)

        response = test_client.get(f'/reset/{token}', follow_redirects=True)

        assert response.status_code == 200
        assert is_reset_password_form(response)


    def test_reset_password_valid_token(test_client, init_database, a_user):
        """
        GIVEN a password reset form for an anonymous user
        WHEN the user submits the form
        THEN the user's password is updated
        AND is redirected to the login page
        """
        token = a_user.generate_token(TokenType.RESET)

        response = reset_password(test_client, token, OTHER_PASSWORD, OTHER_PASSWORD)

        assert response.status_code == 200
        assert is_login_form(response)


    def test_reset_password_invalid_token(test_client, init_database, a_user):
        """
        GIVEN an invalid token
        WHEN the user submits the reset password form
        THEN the user is redirected to the index page
        """
        token = a_user.generate_token(TokenType.RESET, 1)

        response = reset_password(test_client, token + 'a', OTHER_PASSWORD, OTHER_PASSWORD, False)

        assert response.status_code == 302
        assert b'href="/"' in response.data


    def test_reset_password_already_logged_in(test_client, a_user_logged_in):
        """
        WHEN the user accesses reset page with a token
        THEN the user is redirected to the index
        """
        token = a_user_logged_in.generate_token(TokenType.RESET)

        response = test_client.get(f'/reset/{token}')

        assert response.status_code == 302
        assert is_index(response)


    """
    CONFIRMATION EMAIL
    """


    def test_confirm_account_message_after_confirmation(test_client, a_user_logged_in):
        """
        GIVEN a user has not confirmed the account
        WHEN the user clicks the account confirmation link
        THEN the message asking to confirm the account disappeared
        """
        token = a_user_logged_in.generate_token(TokenType.CONFIRM)

        response = test_client.get(f'/confirm/{token}', follow_redirects=True)

        assert response.status_code == 200
        assert b'not confirmed' not in response.data


    @mock.patch(MOCK_EMAIL)
    def test_confirm_account_send_welcome_email(mock_email, test_client, a_user_logged_in):
        """
        GIVEN a user has not confirmed the account
        WHEN the user clicks the account confirmation link
        THEN a welcome email is sent to the user
        """
        token = a_user_logged_in.generate_token(TokenType.CONFIRM)

        test_client.get(f'/confirm/{token}')

        assert mock_email.called


    def test_confirm_account_already_confirmed(test_client, a_user_logged_in):
        """
        GIVEN a user has already confirmed the account
        WHEN the user accesses the confirm url with a token
        THEN redirect to the index page
        """
        token = a_user_logged_in.generate_token(TokenType.CONFIRM)
        test_client.get(f'/confirm/{token}', follow_redirects=True)

        response = test_client.get(f'/confirm/{token}')

        assert response.status_code == 302
        assert is_index(response)


    def test_confirm_invalid_token(test_client, a_user_logged_in):
        """
        GIVEN an invalid account confirmation token
        WHEN the user attempts to confirm the account
        THEN the account is not confirmed
        AND the user is redirected to the index page
        """
        token = a_user_logged_in.generate_token(TokenType.CONFIRM) + 'a'

        response = test_client.get(f'/confirm/{token}', follow_redirects=True)

        assert response.status_code == 200
        assert b'link is invalid' in response.data


    @mock.patch(MOCK_CONFIRM_EMAIL)
    def test_resend_confirm_account(mock_email, test_client, a_user_logged_in):
        """
        GIVEN a signed-in user whose account is unconfirmed
        WHEN the user acceses the index page and requests sending the confirmation email
        THEN an email is sent
        """
        token = a_user_logged_in.generate_token(TokenType.CONFIRM)
        response = test_client.get(f'/confirm-new/{token}', follow_redirects=True)

        assert response.status_code == 200
        assert mock_email.called
        assert b'new account confirmation' in response.data


    @mock.patch(MOCK_CONFIRM_EMAIL)
    def test_resend_confirm_already_confirmed(mock_email, test_client, a_user_logged_in):
        """
        GIVEN a user confirmed its account
        WHEN the user requests a new confirmation link
        THEN do not send an email
        AND flash the account is already confirmed
        """
        token = a_user_logged_in.generate_token(TokenType.CONFIRM)
        test_client.get(f'/confirm/{token}')

        response = test_client.get(f'/confirm-new/{token}', follow_redirects=True)

        assert response.status_code == 200
        assert not mock_email.called
        assert b'already confirmed' in response.data


    @mock.patch(MOCK_CONFIRM_EMAIL)
    def test_resend_confirm_invalid_token(mock_email, test_client, a_user_logged_in):
        """
        WHEN the user requests a new confirmation link with an invalid token
        THEN do not send an email
        AND flash the link is invalid
        """
        token = a_user_logged_in.generate_token(TokenType.CONFIRM) + 'a'
        response = test_client.get(f'/confirm-new/{token}', follow_redirects=True)

        assert response.status_code == 200
        assert not mock_email.called
        assert b'link is invalid' in response.data


    """
    CONFIRMATION EMAIL
    """


    def test_unsubscribe_valid_token(test_client, a_user_logged_in):
        """
        WHEN the clicks the unsubscribe link in an email
        THEN the user is unsubscribed from future emails
        """
        token = a_user_logged_in.generate_token(TokenType.UNSUBSCRIBE)
        response = test_client.get(f'/unsubscribe/{token}', follow_redirects=True)

        assert response.status_code == 200
        assert a_user_logged_in.email_preferences == EmailPreferences(False, False, False)


    def test_unsubscribe_invalid_token(test_client, a_user_logged_in):
        """
        WHEN the unsubscribe token is bad
        THEN a unsubscribed failure message is displayed.
        """
        token = a_user_logged_in.generate_token(TokenType.UNSUBSCRIBE)
        response = test_client.get(f'/unsubscribe/{token}a', follow_redirects=True)

        assert response.status_code == 200
        assert b'link is invalid' in response.data
        assert a_user_logged_in.email_preferences != EmailPreferences(False, False, False)
    '''
