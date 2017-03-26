from django.test import TestCase

from common.gql import get_pk_from_global_id


class GetPkFromGlobalIdTestCase(TestCase):

    def test__when_given_a_proper_id__it_returns(self):
        pk = get_pk_from_global_id('UGVyc29uTm9kZToxMA==')
        self.assertEqual(pk, 10)

    def test__when_given_malformed_id__it_throws(self):
        self.assertRaises(Exception, get_pk_from_global_id, 'foobar')
