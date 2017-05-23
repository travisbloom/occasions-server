from django.test import TestCase

from common.testing_util.get_file_from_web_project import get_file_from_web_project


class GetFilesFromWebProjectTestCase(TestCase):
    def test__i_can_load_files_from_webapp(self):
        file_contents = get_file_from_web_project("uniqueTestFileForBackendFetching.json")
        self.assertEqual(file_contents, '{"hello": "world"}\n')
