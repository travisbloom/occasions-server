from common.relay import Node
from common.test_client_gql.graphql_test_case import GraphQLTestCase
from common.testing_util import build_user_mock_data
from events.factories import EventFactory, AssociatedEventFactory
from events.models import AssociatedEvent
from people.factories import PersonFactory


# TODO add tests for creating new events
class CreateAssociatedEventMutationTestCase(GraphQLTestCase):

    def setUp(self):
        self.file_name = "CreateAssociatedEventMutation.graphql"
        self.user = build_user_mock_data(
            with_transactions=True
        )
        self.default_event = EventFactory(is_default_event=True)
        return super().setUp()

    def test__when_using_existing_event__query_returns_expected_result(self):
        self.generate_or_assert_gql_snapshot_is_equal(self.file_name, variables={
            'input': {
                'event': None,
                'eventId': Node.to_global_id('AssociatedEventNode', self.default_event.pk),
                'receivingPersonId': Node.to_global_id(
                    'PersonNode',
                    self.user.person.from_relationships.first().to_person.pk
                ),
            }
        })

    def test__when_creating_new_event__query_returns_expected_result(self):
        self.generate_or_assert_gql_snapshot_is_equal(self.file_name, variables={
            'input': {
                'event': {
                    'name': 'testEvent',
                    'eventTypes': [
                        Node.to_global_id(
                            'EventTypeNode',
                            event_type.pk
                        )
                        for event_type in self.default_event.event_types.all()
                    ],
                    'nextDate': {
                        'dateStart': self.default_event.next_date.date_start.isoformat()
                    }
                },
                'receivingPersonId': Node.to_global_id(
                    'PersonNode',
                    self.user.person.from_relationships.first().to_person.pk
                ),
            }
        })

    def test__when_passing_unrelated_person__query_errors(self):
        unrelated_person = PersonFactory()
        self.generate_or_assert_gql_snapshot_is_equal(
            self.file_name,
            variables={
                'input': {
                    'event': None,
                    'eventId': Node.to_global_id('AssociatedEventNode', self.default_event.pk),
                    'receivingPersonId': Node.to_global_id(
                        'PersonNode',
                        unrelated_person.pk
                    ),
                }
            })


    def test__when_passing_an_existing_event_that_is_not_a_default__query_errors(self):
        self.different_event = EventFactory(is_default_event=False)
        self.generate_or_assert_gql_snapshot_is_equal(
            self.file_name,
            variables={
                'input': {
                    'event': None,
                    'eventId': Node.to_global_id('AssociatedEventNode', self.different_event.pk),
                    'receivingPersonId': Node.to_global_id(
                        'PersonNode',
                        self.user.person.from_relationships.first().to_person.pk
                    ),
                }
            })

    def test__when_passing_an_event_with_bad_data__query_errors(self):
        self.generate_or_assert_gql_snapshot_is_equal(
            self.file_name,
            variables={
                'input': {
                    'event': {
                        'name': '',
                        'eventTypes': [],
                        'nextDate': {
                            'dateStart': 'foo'
                        }
                    },
                    'receivingPersonId': Node.to_global_id(
                        'PersonNode',
                        self.user.person.from_relationships.first().to_person.pk
                    ),
                }
            })
