from django.test import TestCase

from app.backend.auth.forms import SignupForm


class AuthFormsTests(TestCase):

    def setUp(self):
        self.data = dict(username='username', email='email@email.com', password1='password',
                         password2='password', send_emails=False, agree_terms=True)

    """
    SIGN UP
    """

    def test_signup_form_all_fields_required(self):
        """
        GIVEN six forms, each with one piece of required data missing
        WHEN the forms is validated
        THEN the forms are not valid
        """
        forms_data = [self.data.copy()]*6
        forms_data[0]['username'] = ''
        forms_data[1]['email'] = ''
        forms_data[2]['password1'] = ''
        forms_data[3]['password2'] = ''
        forms_data[4]['send_emails'] = True
        forms_data[5]['agree_terms'] = True

        forms = [SignupForm(data=forms_data[i]) for i in range(6)]

        for form in forms:
            self.assertFalse(form.is_valid())
