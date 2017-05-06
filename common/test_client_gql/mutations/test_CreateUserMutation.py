from common.test_client_gql.graphql_test_case import GraphQLTestCase
from common.testing_util import build_user_mock_data


class CreateUserMutationTestCase(GraphQLTestCase):

    def setUp(self):
        self.file_name = "CreateUserMutation.graphql"
        return super().setUp()

    def test__query_returns_expected_result(self):
        self.generate_or_assert_gql_snapshot_is_equal(self.file_name, variables={
            'input': {
                'username': 'travis@ge.com',
                'password': 'heylookitsasuperlongpassword!'
            }
        })

    def test__when_inputs_are_invalid__query_errors(self):
        self.generate_or_assert_gql_snapshot_is_equal(self.file_name, variables={
            'input': {
                'username': '',
                'password': 'heylookitsasuperlongpassword!'
            }
        })

    def test__when_username_exists__query_errors(self):
        self.generate_or_assert_gql_snapshot_is_equal(self.file_name, variables={
            'input': {
                'username': build_user_mock_data().person.email,
                'password': 'heylookitsasuperlongpassword!'
            }
        })
