from unittest import mock

from django.test import TestCase
from django.urls import reverse

from app.tests.conftest import is_contact_form, create_user, delete_users, A_USERNAME, A_PASSWORD

MOCK_SEND_EMAIL = 'app.backend.contact.views.send_email'


class ContactViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a_user = create_user()
        cls.url = reverse('app:contact.contact_us')

    @classmethod
    def tearDownClass(cls):
        delete_users()

    def test_contact_form_anonymous_user(self):
        """
        GIVEN an anonymous user
        WHEN the contact page is accessed
        THEN the contact form has an email field
        """
        response = self.client.get(self.url, follow=True)

        self.assertTrue(is_contact_form(response))

    def test_contact_form_user(self):
        """
        GIVEN a user logged in
        WHEN the contact page is accessed
        THEN the email field is rendered
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)

        response = self.client.get(self.url, follow=True)

        self.assertTrue(is_contact_form(response, False))

    @mock.patch(MOCK_SEND_EMAIL)
    def test_contact_form_send_email_anynonymous(self, mock_send_email):
        """
        GIVEN an anontmous user
        WHEN the contact form is sent
        THEN send an email to support
        """
        data = dict(first_name='a_name', subject='a_subject', message='a_message', email_address='anemail@test.test')
        response = self.client.post(self.url, data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_send_email.delay.called)
        self.assertIn(b'Thank you for contacting us', response.content)

    @mock.patch(MOCK_SEND_EMAIL)
    def test_contact_form_send_email_user(self, mock_send_email):
        """
        GIVEN a user logged in
        WHEN the contact form is sent
        THEN send an email to support
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        data = dict(first_name='a_name', subject='a_subject', message='a_message')
        response = self.client.post(self.url, data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_send_email.delay.called)
        self.assertIn(b'Thank you for contacting us', response.content)

    @mock.patch(MOCK_SEND_EMAIL)
    def test_contact_form_send_email_redirect(self, mock_send_email):
        """
        WHEN the contact form is sent
        THEN the user is redirected to the index page
        """
        data = dict(first_name='a_name', subject='a_subject', message='a_message', email_address='anemail@test.test')
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('app:main.index'))
