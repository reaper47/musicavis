import json

from django.test import TestCase
from django.urls import reverse

from musicavis.settings import EXPORTS_DIR
from app.tests.conftest import create_user, A_USERNAME, A_PASSWORD, is_user_index, is_anonymous_index, delete_users


class MainViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a_user = create_user()
        cls.url_index = reverse('app:main.index')

    @classmethod
    def tearDownClass(cls):
        delete_users()

    """
    INDEX
    """

    def test_index_anonymous(self):
        """
        WHEN an anonymous user accesses the website
        THEN display the website of the product
        """
        response = self.client.get(self.url_index, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_anonymous_index(response))

    def test_user_index(self):
        """
        WHEN a user is logged in
        THEN display the index page of the application
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)

        response = self.client.get(self.url_index, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_user_index(response))

    """
    SITEMAP
    """

    def test_sitemap_anonymous(self):
        """
        WHEN requesting the sitemap page
        THEN return the sitemap page
        """
        response = self.client.get(reverse('app:main.sitemap'), follow=True)

        data = ['Home', 'Features', 'Pricing', 'Our team', 'Contact us',
                'Careers', 'News', 'Privacy Policy', 'Terms of Use']
        assert response.status_code == 200
        assert all([x.encode() in response.content for x in data])

    """
    NOTIFICATIONS
    """

    def test_notifications_get_notifications(self):
        """
        GIVEN a user logged in with two notifications
        WHEN the notifications route is called
        THEN return the notifications as a JSON payload
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        self.a_user.profile.add_notification('test1', {'test': 1})
        self.a_user.profile.add_notification('test2', {'test': 2})
        payload_expected = {
            'names': ['test1', 'test2'],
            'data': [{'test': 1}, {'test': 2}],
        }

        response = self.client.get(reverse('app:main.notifications'))
        payload = json.loads(response.content)
        payload['data'] = [json.loads(x) for x in payload['data']]

        for field in ['names', 'data', 'timestamps']:
            self.assertEqual(len(payload[field]), 2)
        self.assertEqual(payload['names'], payload_expected['names'])
        self.assertEqual(payload['data'], payload_expected['data'])

    """
    EXPORTS TESTS
    """

    def test_exports_file(self):
        """
        WHEN the user wants to download a file
        THEN file is sent to the user with the appropriate HTTP Headers
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        exported_file = export_file('test1.txt')

        response = self.client.get(reverse('app:main.export', args=(exported_file,)))

        self.assertEqual(response._headers['content-type'][1], 'text/plain')
        self.assertEqual(int(response._headers['content-length'][1]), 32)
        self.assertEqual(response._headers['content-disposition'][1], f'attachment; filename={exported_file}')

    def test_exports_delete_notification(self):
        """
        GIVEN a user has an exported file notification
        WHEN the user retrieves the file after clicking the notification
        THEN the user's notification is deleted
        """
        self.client.login(username=A_USERNAME, password=A_PASSWORD)
        exported_file = export_file('test2.txt')
        self.a_user.profile.add_notification(f"export_practice_task_{exported_file.split('.')[1]}",
                                             {'task_id': 'wewedsdf-wewe', 'file_name': exported_file})

        self.client.get(reverse('app:main.export', args=(exported_file,)))

        self.assertEqual(len(self.a_user.profile.notifications.all()), 0)


def export_file(fname: str):
    with open(f'{EXPORTS_DIR}/{fname}', 'w') as f:
        f.write('This is a text of 32 characters\n')
    return fname
