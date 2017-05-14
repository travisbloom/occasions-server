from django.test import TestCase

from common.testing_util import build_user_mock_data


class TransactionTestCase(TestCase):

    def setUp(self):
        super().setUp()
        build_user_mock_data(
            with_products=False,
            with_relationships=False,
            with_associated_events=False,
        )

    # def test__when_receiving_person_not_related_to_user__raises_error(self):

