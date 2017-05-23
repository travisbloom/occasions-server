import difflib
import inspect
import os
from typing import Any

import colored
import simplejson
from colored import stylize
from graphql_relay.utils import unbase64

from common.utils.json import JSON


def colored_diff(diff):
    for line in diff:
        if line.startswith('+'):
            yield stylize(line, colored.fg("green"))
        elif line.startswith('-'):
            yield stylize(line, colored.fg("red"))
        elif line.startswith('^'):
            yield stylize(line, colored.fg("blue"))
        else:
            yield line


class SnapshotGenerator:
    def __init__(self, new_snapshot_data, snapshot_directory, snapshot_filename, is_graphql, mock_auto_dates):
        self.is_graphql = is_graphql
        self.mock_auto_dates = mock_auto_dates
        os.makedirs(snapshot_directory, exist_ok=True)
        self.file_path = os.path.join(snapshot_directory, snapshot_filename)
        if not os.path.isfile(self.file_path):
            self.write_to_snapshot_file('')
        self.new_snapshot_data = self.transform_data(new_snapshot_data)
        self.error_stack = None
        self.error_locations = None

    @staticmethod
    def decode(val: str):
        # FIXME there are places where we include props called ID in the gql query that are the actual pks, not the relay node ids (see hotel explainer snapshot)
        try:
            return '{} ({})'.format(val, unbase64(val))
        except:
            return val

    def transform_data(self, data):
        if 'errors' in data:
            self.error_stack = data['errors'][0].pop('stack')
            self.error_locations = data['errors'][0].pop('locations')
            if 'data' in data['errors'][0]:
                data['errors'][0].pop('message')

        def transform_value(val):
            if isinstance(val, dict):
                if self.is_graphql and isinstance(val, dict):
                    for key in ('id', 'cursor', 'endCursor', 'startCursor'):
                        if val.get(key, None):
                            val[key] = self.decode(val[key])
                if self.mock_auto_dates:
                    for key in ('datetimeCreated', 'datetimeUpdated'):
                        if val.get(key, None):
                            val[key] = 'MOCK_OUT_AUTO_DATES'
                return {
                    k: transform_value(v)
                    for k, v in val.items()
                }
            elif isinstance(val, list):
                return list(transform_value(x) for x in val)
            elif isinstance(val, tuple):
                return list(transform_value(x) for x in val)
            else:
                return val
        return transform_value(data)

    def execute(self, should_update=False):
        existing_json = self.get_existing_snapshot_json()
        new_snapshot_json = simplejson.dumps(self.new_snapshot_data, sort_keys=True, indent=4)
        if existing_json != new_snapshot_json:
            if should_update:
                self.write_to_snapshot_file(new_snapshot_json)
                return True
            else:
                self.diff_and_print_message(existing_json, new_snapshot_json)
                return False
        return True

    def get_existing_snapshot_json(self):
        with open(self.file_path, "r") as snapshot_file:
            return snapshot_file.read()

    def write_to_snapshot_file(self, content: str):
        with open(self.file_path, "w") as snapshot_file:
            snapshot_file.write(content)

    def diff_and_print_message(self, existing_snapshot_json, new_snapshot_json):
        generated_snapshot = new_snapshot_json.splitlines(keepends=True)
        existing_snapshot = existing_snapshot_json.splitlines(keepends=True)
        diff = difflib.unified_diff(existing_snapshot, generated_snapshot, self.file_path, 'new_snapshot')
        print(''.join(colored_diff(diff)), end="")
        if self.error_stack:
            print("\n Error Stack:\n{}".format(JSON.stringify(self.error_stack)))
        if self.error_locations:
            print("\n Error Locations:\n{}".format(JSON.stringify(self.error_locations)))
        print("\nIf this is the expected result, you can update this snapshot by running the testing suite with the env variable OVERRIDE_SNAPSHOTS=true")


def generate_or_assert_snapshot_is_equal(
        new_snapshot_data: Any,
        parent_method_name=None,
        parent_method_file_name=None,
        mock_auto_dates=True,
        is_graphql=False):
    """Checks a snapshotted value against an existing"""
    parent_method_name = parent_method_name or inspect.stack()[1][3]
    parent_method_file_name = parent_method_file_name or inspect.stack()[1][1]
    snapshot_directory = os.path.join(os.path.dirname(parent_method_file_name), '__snapshots__')
    snapshot_filename = "{}__{}.json".format(os.path.basename(parent_method_file_name), parent_method_name)
    return SnapshotGenerator(
        new_snapshot_data,
        snapshot_directory=snapshot_directory,
        snapshot_filename=snapshot_filename,
        mock_auto_dates=mock_auto_dates,
        is_graphql=is_graphql
    ).execute(should_update=os.environ.get('OVERRIDE_SNAPSHOTS', 'false') == 'true')