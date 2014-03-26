from django.contrib.admin import AdminSite
from django.test import TestCase

from orderable.admin import OrderableAdmin
from orderable.tests.models import Task


class OrderableAdminTest(TestCase):
    def test_get_url_name(self):
        expected_name = 'adminadmin_tests_task_reorder'
        admin_site = AdminSite()

        url_name = OrderableAdmin(Task, admin_site).get_url_name()
        self.assertEqual(url_name, expected_name)
