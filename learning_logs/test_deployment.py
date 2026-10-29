from django.core.management import call_command
from django.test import TestCase, override_settings


class StaticDeploymentTests(TestCase):
    @override_settings(DEBUG=False)
    def test_collected_admin_css_is_served_in_production_mode(self):
        call_command('collectstatic', interactive=False, verbosity=0)

        self.assertEqual(self.client.get('/static/admin/css/base.css').status_code, 200)
