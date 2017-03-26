from django.test import TestCase

from common.test_client_gql.graphql_test_case import GraphQLTestCase
from common.testing_util import build_user_mock_data
from common.relay import Node

from people.factories import PersonFactory


# TODO add tests for creating new events
class CreateAssociatedEventMutationTestCase(GraphQLTestCase):

    def setUp(self):
        self.file_name = "CreateAssociatedEventMutation.graphql"
        self.user = build_user_mock_data(
            with_transactions=True
        )
        return super().setUp()

    def test__when_using_existing_event__query_returns_expected_result(self):
        associated_event = self.user.person.created_events.first()
        self.generate_or_assert_gql_snapshot_is_equal(self.file_name, variables={
            'input': {
                'event': None,
                'eventId': Node.to_global_id('AssociatedEventNode', associated_event.pk),
                'receivingPersonId': Node.to_global_id(
                    'PersonNode',
                    associated_event.receiving_person.pk
                ),
            }
        })

    def test__when_passing_unrelated_person__query_errors(self):
        associated_event = self.user.person.created_events.first()
        unrelated_person = PersonFactory()
        self.generate_or_assert_gql_snapshot_is_equal(
            self.file_name,
            expected_code=200,
            variables={
                'input': {
                    'event': None,
                    'eventId': Node.to_global_id('AssociatedEventNode', associated_event.pk),
                    'receivingPersonId': Node.to_global_id(
                        'PersonNode',
                        unrelated_person.pk
                    ),
                }
            })
