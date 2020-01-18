import json

from django.test import TestCase

from app.models.user import User
from app.models.notification import Notification
from app.tests.conftest import create_user, A_USERNAME, A_PASSWORD, AN_EMAIL


class UserModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        User.objects.all().delete()
        super(UserModelTests, cls).setUpClass()

    def test_notification_get_data(self):
        """
        WHEN getting a notification's data
        THEN return the data as JSON
        """
        payload = dict(test=1)
        user = create_user(A_USERNAME, A_PASSWORD, AN_EMAIL)
        notification = Notification(name='test', user_object=user, timestamp=23.4324324,
                                    payload_json=json.dumps(payload))

        data = notification.get_data()

        self.assertEqual(data, payload)
