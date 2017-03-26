import simplejson
import inspect
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from common.testing_util import get_file_from_web_project, generate_or_assert_snapshot_is_equal
from common.schema import schema
from common.views import OccasionsGraphQLView


class GraphQLTestCase(TestCase):

    def setUp(self):
        self.requestFactory = RequestFactory()
        self.view = OccasionsGraphQLView.as_view(schema=schema)

    def generate_or_assert_gql_snapshot_is_equal(
        self,
        file_name,
        variables=None,
        endpoint='graphql',
        expected_code=200
    ):
        file_contents = get_file_from_web_project(file_name)
        request = self.requestFactory.post(endpoint, {
            'query': file_contents,
            'variables': simplejson.dumps(variables or {})
        })

        request.user = self.user
        response = self.view(request)
        import pdb
        pdb.set_trace()
        if response.status_code != expected_code:
            print(response.content.decode())
        is_snapshot_equal = generate_or_assert_snapshot_is_equal(
            simplejson.loads(response.content.decode()),
            parent_method_name=inspect.stack()[1][3],
            parent_method_file_name=inspect.stack()[1][1]
        )

        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(is_snapshot_equal, True)
