import pendulum
from django.test import TestCase


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        mocked_now = pendulum.create(2017, 1, 1, 1)
        pendulum.set_test_now(mocked_now)


