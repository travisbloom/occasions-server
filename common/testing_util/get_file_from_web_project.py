import glob
import os
from django.conf import settings

web_project_dir = os.path.abspath(os.path.join(settings.BASE_DIR, "..", "occasions-web"))
print(web_project_dir)


def get_file_from_web_project(file_name):
    files = [file_name for file_name in glob.glob(
        "{}/**/{}".format(web_project_dir, file_name), recursive=True)]
    if not files:
        raise Exception('No file found for {}'.format(file_name))
    if len(files) > 1:
        raise Exception('more than one file found for {}'.format(file_name))
    with open(files[0], 'r') as file_contents:
        return file_contents.read()
