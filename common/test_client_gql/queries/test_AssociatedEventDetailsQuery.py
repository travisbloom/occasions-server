from common.relay import Node
from common.test_client_gql.graphql_test_case import GraphQLTestCase
from common.testing_util import build_user_mock_data


class AssociatedEventDetailsQueryTestCase(GraphQLTestCase):
    def setUp(self):
        self.file_name = "AssociatedEventDetailsQuery.graphql"
        self.user = build_user_mock_data(
            with_associated_events=True
        )
        return super().setUp()

    def test__query_returns_expected_result(self):
        self.generate_or_assert_gql_snapshot_is_equal(self.file_name, variables={
            'associatedEventId': Node.to_global_id('AssociatedEventNode', 1)
        })
