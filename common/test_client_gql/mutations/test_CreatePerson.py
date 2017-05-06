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
    'first_name': 'Travis',
    'last_name': 'Bloom',
    'email': 'trigga@trey.com'
}


class CreatePersonMutationTestCase(GraphQLTestCase):

    def setUp(self):
        self.file_name = "CreatePersonMutation.graphql"
        self.user = build_user_mock_data(
            with_relationships=True
        )
        return super().setUp()

    def test__valid_input_submitted__query_returns_successfully(self):
        person = self.user

        self.generate_or_assert_gql_snapshot_is_equal(
            self.file_name,
            variables={
                'input': {
                    **valid_person_payload,
                    'locations': [
                        valid_location_payload
                    ]
                }
            })
