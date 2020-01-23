import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from app.models.practice import Goal, Practice, Exercise, Improvement, Positive
from app.backend.utils.instruments import populate_db
from .test_forms import A_GOAL_NAME, A_POSITIVE_NAME, AN_IMPROVEMENT_NAME
from app.tests.conftest import (A_USERNAME, A_PASSWORD, create_user, delete_users, is_new_practice_form,
                                is_practice_session, AN_INSTRUMENT)

data = {
    'goal_0': A_GOAL_NAME, 'positives_0': A_POSITIVE_NAME,
    'improvement_0': AN_IMPROVEMENT_NAME, 'notes': 'notes',
    'exercise_0_name': 'C-Arpeggio', 'exercise_0_bpm_start': 60,
    'exercise_0_bpm_end': 75, 'exercise_0_minutes': 5
}


class PracticeViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a_user = create_user()
        cls.url_practice = reverse('app:practice.new')
        cls.url_list = reverse('app:practice.list_past_practices')
        populate_db()

    @classmethod
    def tearDownClass(cls):
        delete_users()

    def setUp(self):
        self.client.login(username=A_USERNAME, password=A_PASSWORD)

    """
    NEW PRACTICE SESSION TESTS
    """

    def test_new_practice_session_get(self):
        """
        WHEN a new practice session is requested
        THEN display the form to select an instrument
        """
        response = self.client.get(self.url_practice, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_new_practice_form(response))

    def test_new_practice_session_post(self):
        """
        GIVEN a user has selected an instrument in the new practice form
        WHEN the user submits the form
        THEN the newly created practice session is displayed
        """
        response = self.client.post(self.url_practice, data=dict(instrument='trombone'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_practice_session(response))

    """
    UPDATE PRACTICE SESSION TESTS
    """

    def test_update_model(self):
        """
        GIVEN a user with a new practice session
        WHEN the user saves the practice form
        THEN the form is saved
        """
        self.a_user.profile.new_practice('trombone')
        practice = self.a_user.profile.practices.last()

        response = self.client.post(reverse('app:practice.session', args=[practice.pk]), data=data, follow=True)
        json_response = json.loads(response.content)

        self.assertEqual(json_response['status_code'], 200)

    def test_update_model_test_exercsises(self):
        """
        GIVEN a user with a populated practice session
        WHEN the user adds duplicate elements
        THEN there are no inconsistencies in the practice's exercises
        """
        self.a_user.profile.new_practice('trombone')
        practice = self.a_user.profile.practices.last()
        url = reverse('app:practice.session', args=[practice.pk])
        self.client.post(url, data=data, follow=True)

        new_data = {
            'exercise_0_name': 'C-Arpeggio', 'exercise_0_bpm_start': 60,
            'exercise_0_bpm_end': 75, 'exercise_0_minutes': 5,
            'exercise_1_name': 'C-Arpeggio', 'exercise_1_bpm_start': 60,
            'exercise_1_bpm_end': 75, 'exercise_1_minutes': 10,
            'exercise_2_name': 'C-Arpeggio', 'exercise_2_bpm_start': 60,
            'exercise_2_bpm_end': 75, 'exercise_2_minutes': 5,
            'exercise_3_name': 'C-Arpeggio', 'exercise_3_bpm_start': 70,
            'exercise_3_bpm_end': 75, 'exercise_3_minutes': 5
        }
        self.client.post(url, data=new_data, follow=True)

        self.assertEqual(practice.goals.count(), 0)
        self.assertEqual(practice.improvements.count(), 0)
        self.assertEqual(practice.positives.count(), 0)
        self.assertEqual(practice.exercises.count(), 3)

    def test_update_model_test_name_fields(self):
        """
        GIVEN a user with a populated practice session
        WHEN the user adds duplicate elements
        THEN there are no inconsistencies in the name fields
        """
        self.a_user.profile.new_practice('trombone')
        practice = self.a_user.profile.practices.last()
        url = reverse('app:practice.session', args=[practice.pk])
        self.client.post(url, data=data, follow=True)

        new_data = {
            'goal_0': 'C-Arpeggio',
            'goal_1': 'toeer',
            'positive_0': 'D-Arpeggio',
            'positive_1': '75',
            'improvement_0': 'H-Arpeggio',
            'improvement_1': 'boo',
            'goal_2': 'T-Arpeggio',
            'positive_2': '90'
        }
        self.client.post(url, data=new_data, follow=True)

        self.assertEqual(practice.goals.count(), 3)
        self.assertEqual(practice.improvements.count(), 2)
        self.assertEqual(practice.positives.count(), 3)

    """
    DELETE PRACTICE SESSION TESTS
    """

    def test_delete_session_anonymous_user(self):
        """
        GIVEN a practice in the database
        WHEN an anoynmous attempts to delete a session
        THEN do not delete the session
        AND redirect to the index
        """
        self.a_user.profile.new_practice('trombone')
        practice = self.a_user.profile.practices.last()
        num_practice = Practice.objects.count()
        self.client.logout()

        response = self.client.delete(reverse('app:practice.session', args=[practice.pk]))

        self.assertIn(reverse('app:auth.login'), response.url)
        self.assertEqual(Practice.objects.count(), num_practice)

    def test_delete_session_only_for_user(self):
        """
        GIVEN two users and one practice session each
        WHEN the 1st user attempts to delete the practice session of the 2nd user
        AND the 1st user deletes his practice session
        THEN do not delete the 2nd user's practice
        BUT delete the 1st user's practice
        """
        other_user = create_user('bob', 'bob@bob.bob', 'fried-chicken')
        self.a_user.profile.new_practice('cheese')
        other_user.profile.new_practice('cheese')
        practice = self.a_user.profile.practices.last()
        other_practice = other_user.profile.practices.last()

        self.client.delete(reverse('app:practice.session', args=[other_practice.pk]))
        self.client.delete(reverse('app:practice.session', args=[practice.pk]))

        self.assertEqual(User.objects.filter(username='bob').first().profile.practices.count(), 1)
        self.assertEqual(User.objects.filter(username=A_USERNAME).first().profile.practices.count(), 0)

    """
    LIST PRACTICE SESSION TESTS
    """

    def test_list_practices(self):
        """
        GIVEN a user has three practice sessions
        WHEN the user consults previous practices
        THEN display a paginated list of exercises
        """
        npractices = 3
        for i in range(npractices):
            self.a_user.profile.new_practice(AN_INSTRUMENT)

        response = self.client.get(self.url_list, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode().count(AN_INSTRUMENT), npractices)

    def test_list_practices_user_when_user_has_none(self):
        """
        GIVEN a user has no practices
        WHEN the list of previous practices is consulted
        THEN display a link to creating a new practice session
        """
        response = self.client.get(self.url_list, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/practice', response.content)

    def test_list_practices_display_total_time_practiced(self):
        """
        GIVEN a user practiced 5 exercises each lasting 25 minutes
        WHEN the list of previous practices is consulted
        THEN display the total practice in hours and minutes
        """
        self.a_user.profile.new_practice(AN_INSTRUMENT)
        a_practice = self.a_user.profile.practices.first()
        for i in range(5):
            name = chr(ord('C') + i)
            a_practice.exercises.add(Exercise.objects.create(name=name, bpm_start=i, bpm_end=i, minutes=25))

        response = self.client.get(self.url_list, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'2h05', response.content)

    """
    CONSULT PRACTICE SESSION TESTS
    """

    def test_view_practice_session_multiple_entries(self):
        """
        GIVEN a practice session with a few entities stored
        WHEN its page is accessed
        THEN display the few entities
        """
        practice = self.a_user.profile.new_practice(AN_INSTRUMENT)
        practice.goals.add(Goal.objects.create(name=A_GOAL_NAME))
        practice.improvements.add(Improvement.objects.create(name=AN_IMPROVEMENT_NAME))
        practice.positives.add(Positive.objects.create(name=A_POSITIVE_NAME))

        response = self.client.get(reverse('app:practice.session', args=[practice.pk]), follow=True)

        names_expected = [A_GOAL_NAME, A_POSITIVE_NAME, AN_IMPROVEMENT_NAME]
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(x.encode() in response.content for x in names_expected))
