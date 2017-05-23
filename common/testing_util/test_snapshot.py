import simplejson
from django.test import TestCase

from common.testing_util.get_file_from_web_project import get_file_from_web_project
from common.testing_util.snapshot import generate_or_assert_snapshot_is_equal


class GetFilesFromWebProjectTestCase(TestCase):
    def test__i_can_load_files_from_webapp(self):
        file_contents = get_file_from_web_project("uniqueTestFileForBackendFetching.json")
        self.assertEqual(
            generate_or_assert_snapshot_is_equal(
                simplejson.loads(file_contents)
            ),
            True
        )
