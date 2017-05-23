from common.relay import Node
from common.test_client_gql.graphql_test_case import GraphQLTestCase
from common.testing_util import build_user_mock_data

valid_location_payload = {
    'streetAddressLine1': 'First Street Line',
    'streetAddressLine2': 'Second Street Line',
    'postalCode': '10011',
    'city': 'NYC',
    'state': 'NY',
}

valid_person_payload = {
    'firstName': 'Travis',
    'lastName': 'Bloom',
    'email': 'trigga@trey.com',
    'birthDate': '2017-02-23',
    'relationshipType': Node.to_global_id(
        'RelationshipTypeNode',
        'sibling_to_sibling'
    ),
    'gender': 'MALE',
}


class CreatePersonMutationTestCase(GraphQLTestCase):
    def setUp(self):
        self.file_name = "CreatePersonMutation.graphql"
        self.user = build_user_mock_data()
        return super().setUp()

    def test__valid_input_submitted__query_returns_successfully(self):
        person = self.user

        self.generate_or_assert_gql_snapshot_is_equal(
            self.file_name,
            variables={
                'input': {
                    **valid_person_payload,
                    'locations': [
                        valid_location_payload,
                        {
                            **valid_location_payload,
                            'streetAddressLine1': 'Second Street Address'
                        }
                    ]
                }
            })

    def test__invalid_input_submitted__query_errors(self):
        person = self.user

        self.generate_or_assert_gql_snapshot_is_equal(
            self.file_name,

            variables={
                'input': {
                    'firstName': '',
                    'lastName': '',
                    'email': 'trigga',
                    'birthDate': 'foo23',
                    'relationshipType': Node.to_global_id(
                        'RelationshipTypeNode',
                        'foo'
                    ),
                    'gender': 'MLE',
                    'locations': [
                        {
                            'streetAddressLine1': '',
                            'postalCode': '',
                            'city': '',
                            'state': '',
                        }
                    ]
                }
            })

    def test__no_locations_submitted__query_errors(self):
        person = self.user

        self.generate_or_assert_gql_snapshot_is_equal(
            self.file_name,

            variables={
                'input': {
                    **valid_person_payload,
                    'locations': []
                }
            })
