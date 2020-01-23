from django.test import TestCase
from django.urls import reverse

from app.models.practice import Exercise
from app.tests.conftest import (A_USERNAME, OTHER_PASSWORD, OTHER_USERNAME, A_PASSWORD, create_user_with_a_practice,
                                delete_users, create_user)


class DashboardViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a_user = create_user()
        cls.a_user_with_a_practice = create_user_with_a_practice()
        cls.url = reverse('app:dashboard.index')

    @classmethod
    def tearDownClass(cls):
        delete_users()

    def test_dashboard_no_practices(self):
        """
        GIVEN a user has not practiced yet
        WHEN the dashboard is accessed
        THEN a message of no practices is displayed
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)

        response = self.client.get(self.url, follow=True)

        text = response.content.decode().lower()
        self.assertEqual(response.status_code, 200)
        self.assertIn('start practicing', text)
        self.assertNotIn('statistics', text)

    def test_dashboard_statistics(self):
        """
        GIVEN a user with a couple of practices
        WHEN the dashboard is accessed
        THEN metrics on the user's practices are displayed
        """
        self.client.login(username=OTHER_USERNAME, password=OTHER_PASSWORD)
        exercise = Exercise.objects.create(name='C', bpm_start=40, bpm_end=80, minutes=5)
        self.a_user_with_a_practice.profile.practices.first().exercises.add(exercise)

        response = self.client.get(self.url, follow=True)

        text = response.content.decode().lower()
        self.assertEqual(response.status_code, 200)
        self.assertIn('table id="dashboard__table-statistics"', text)
        self.assertIn('total practice time', text)
        self.assertIn('median number of exercises', text)
