import inspect

import simplejson
from django.test import RequestFactory

from common.schema import schema
from common.testing_util import get_file_from_web_project, generate_or_assert_snapshot_is_equal
from common.testing_util.base_test_case import BaseTestCase
from common.utils.deep_transform import deep_transform
from common.views import OccasionsGraphQLView


class GraphQLTestCase(BaseTestCase):
    fixtures = ('event_types',)

    def setUp(self):
        self.requestFactory = RequestFactory()
        self.view = OccasionsGraphQLView.as_view(schema=schema)


    def load_json(self, response):
        json = simplejson.loads(response.content.decode())
        return deep_transform(
            json,
            lambda key, val: key in ['datetimeCreated', 'datetimeUpdated'],
            lambda key, val: 'MOCKED_AUTO_GENERATED_DATETIME'
        )

    def generate_or_assert_gql_snapshot_is_equal(
        self,
        file_name,
        variables=None,
        endpoint='graphql',
        should_error=False
    ):
        file_contents = get_file_from_web_project(file_name)
        request = self.requestFactory.post(endpoint, {
            'query': file_contents,
            'variables': simplejson.dumps(variables or {})
        })

        request.user = self.user if hasattr(self, 'user') else None
        response = self.view(request)

        is_snapshot_equal = generate_or_assert_snapshot_is_equal(
            self.load_json(response),
            parent_method_name=inspect.stack()[1][3],
            parent_method_file_name=inspect.stack()[1][1],
            is_graphql=True
        )

        self.assertEqual(response.status_code != 200, should_error)
        self.assertEqual(is_snapshot_equal, True)
