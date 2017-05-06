from django.test import TestCase

from common.gql import get_pk_from_global_id
from common.gql.get_pk_from_global_id import convert_input_global_ids_to_pks


class GetPkFromGlobalIdTestCase(TestCase):

    def test_get_pk_from_global_id__when_given_a_proper_id__it_returns(self):
        pk = get_pk_from_global_id('UGVyc29uTm9kZToxMA==')
        self.assertEqual(pk, 10)

    def test_get_pk_from_global_id__when_given_malformed_id__it_throws(self):
        self.assertRaises(Exception, get_pk_from_global_id, 'foobar')

    def test_convert_input_global_ids_to_pks__when_given_input__it_returns(self):
        passed_input = {
            'foo': 'bar',
            'array': [
                {'baz': 'haz', 'some_id': 'UGVyc29uTm9kZToxMA=='}
            ]
        }
        expected_output = {
            'foo': 'bar',
            'array': [
                {'baz': 'haz', 'some_id': 10}
            ]
        }
        self.assertEqual(convert_input_global_ids_to_pks(passed_input), expected_output)
