from common.test_client_gql.graphql_test_case import GraphQLTestCase
from common.testing_util import build_user_mock_data


class CreateStripeUserMutationTestCase(GraphQLTestCase):
    def setUp(self):
        self.file_name = "CreateStripeUserMutation.graphql"
        self.user = build_user_mock_data(
            with_transactions=True
        )
        return super().setUp()

    def test__when_user_has_stripe_id__query_errors(self):
        self.generate_or_assert_gql_snapshot_is_equal(
            self.file_name,
            variables={
                'input': {
                    'stripTransactionId': 'NOT_A_REAL_TRANSACTION_ID',
                    'email': self.user.person.email
                }
            })
