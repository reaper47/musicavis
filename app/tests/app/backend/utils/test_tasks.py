from django.test import TestCase

from app.tests.conftest import create_user, delete_users


class TasksModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a_profile = create_user()

    @classmethod
    def tearDownClass(cls):
        delete_users()

    '''
    @mock.patch('polls.models.user.export_practices')
    def test_export_practices_call_user_export_practices(self):
        """
        WHEN launching a task
        THEN the task is added to the database
        """
        mock_task.enqueue.return_value = JobMock()

        a_user.launch_task('name', 'description')

        task = Task.query.all()[-1]
        assert task.name == 'name'
        assert task.description == 'description'

    @mock.patch(MOCK_CURRENT_APP_QUEUE)
    def test_export_practices_add_to_db(self):
        """
        WHEN launching a task
        THEN the task is added to the database
        """
        mock_task.enqueue.return_value = JobMock()

        a_user.launch_task('name', 'description')

        task = Task.query.all()[-1]
        assert task.name == 'name'
        assert task.description == 'description'
    '''
