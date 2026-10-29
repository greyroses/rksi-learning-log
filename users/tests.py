from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserFlowTests(TestCase):
    def test_registration_creates_and_logs_in_user(self):
        response = self.client.post(
            reverse('users:register'),
            {'username': 'new-learner', 'password1': 'complex-test-password-123', 'password2': 'complex-test-password-123'},
        )

        self.assertRedirects(response, reverse('learning_logs:topics'))
        self.assertTrue(get_user_model().objects.filter(username='new-learner').exists())

    def test_logout_rejects_get(self):
        user = get_user_model().objects.create_user('logout-user', password='test-password')
        self.client.force_login(user)

        self.assertEqual(self.client.get(reverse('users:logout')).status_code, 405)
