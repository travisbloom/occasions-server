from django.test import TestCase

from common.test_client_gql.graphql_test_case import GraphQLTestCase
from common.testing_util import build_user_mock_data
from common.relay import Node

from products.models import Product


class CreateTransactionMutationTestCase(GraphQLTestCase):

    def setUp(self):
        self.file_name = "CreateTransactionMutation.graphql"
        self.user = build_user_mock_data(
            with_transactions=True
        )
        return super().setUp()

    def test__query_returns_expected_result(self):
        product = Product.objects.first()
        associated_event = self.user.person.created_events.first()
        self.generate_or_assert_gql_snapshot_is_equal(self.file_name, variables={
            'input': {
                'productId': Node.to_global_id('ProductNode', product.pk),
                'associatedEventId': Node.to_global_id(
                    'AssociatedEventNode',
                    associated_event.pk
                ),
                'associatedLocationId': Node.to_global_id(
                    'AssociatedEventNode',
                    associated_event.receiving_person.associated_locations.first().pk
                ),
                'receivingPersonId': Node.to_global_id(
                    'AssociatedEventNode',
                    associated_event.receiving_person.pk
                ),
                'productNotes': 'word dawg',
            }
        })

    def test__when_location_is_not_creator_or_receiver__query_errors(self):
        product = Product.objects.first()
        associated_event = self.user.person.created_events.first()
        other_associated_event = self.user.person.created_events.all()[1]
        self.generate_or_assert_gql_snapshot_is_equal(self.file_name, variables={
            'input': {
                'productId': Node.to_global_id('ProductNode', product.pk),
                'associatedEventId': Node.to_global_id(
                    'AssociatedEventNode',
                    associated_event.pk
                ),
                'associatedLocationId': Node.to_global_id(
                    'AssociatedEventNode',
                    other_associated_event.receiving_person.associated_locations.first().pk
                ),
                'receivingPersonId': Node.to_global_id(
                    'AssociatedEventNode',
                    associated_event.receiving_person.pk
                ),
                'productNotes': 'word dawg',
            }
        })
