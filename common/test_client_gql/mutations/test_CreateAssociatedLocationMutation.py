from common.relay import Node
from common.test_client_gql.graphql_test_case import GraphQLTestCase
from common.testing_util import build_user_mock_data
from people.factories import PersonFactory

valid_location_payload = {
    'streetAddressLine1': 'First Street Line',
    'streetAddressLine2': 'Second Street Line',
    'postalCode': '10011',
    'city': 'NYC',
    'state': 'NY',
}


class CreateAssociatedLocationMutationTestCase(GraphQLTestCase):

    def setUp(self):
        self.file_name = "CreateAssociatedLocationMutation.graphql"
        self.user = build_user_mock_data()
        return super().setUp()

    def test__valid_input_submitted__query_returns_successfully(self):
        person = self.user.person.from_relationships.first().to_person

        self.generate_or_assert_gql_snapshot_is_equal(
            self.file_name,
            variables={
                'input': {
                    'personId': Node.to_global_id('PersonNode', person.pk),
                    'location': valid_location_payload
                }
            })

    def test__invalid_input_submitted__query_errors(self):
        person = self.user.person.from_relationships.first().to_person

        self.generate_or_assert_gql_snapshot_is_equal(
            self.file_name,
            variables={
                'input': {
                    'personId': Node.to_global_id('PersonNode', person.pk),
                    'location': {
                        'streetAddressLine1': '',
                        'streetAddressLine2': 'Second Street Line',
                        'postalCode': 'sdsdd',  # TODO add postal code validation
                        'city': 'NYC',
                        'state': 'NOTASTATE',  # TODO add state validation
                    }
                }
            })

    def test__unrelated_person__query_errors(self):
        person = PersonFactory()
        self.generate_or_assert_gql_snapshot_is_equal(
            self.file_name,
            variables={
                'input': {
                    'personId': Node.to_global_id('PersonNode', person.pk),
                    'location': valid_location_payload
                }
            })
