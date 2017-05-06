from common.relay import Node
from common.test_client_gql.graphql_test_case import GraphQLTestCase
from common.testing_util import build_user_mock_data


class TransactionDetailsQueryTestCase(GraphQLTestCase):

    def setUp(self):
        self.file_name = "TransactionDetailsQuery.graphql"
        self.user = build_user_mock_data(
            with_transactions=True
        )
        return super().setUp()

    def test__query_returns_expected_result(self):
        self.generate_or_assert_gql_snapshot_is_equal(self.file_name, variables={
            'transactionId': Node.to_global_id('TransactionNode', 1),
        })
