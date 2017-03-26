import inspect
import os
import simplejson
from jsondiff import diff


def generate_json(snapshot_json):
    return simplejson.dumps(snapshot_json, sort_keys=True, indent=4)


def generate_snapshot_file(snapshot_json, file_path, file_name):
    with open(file_path, "w") as snapshot_file:
        snapshot_file.write(generate_json(snapshot_json))
    print('snapshot generated: {}'.format(file_name))


def generate_or_assert_snapshot_is_equal(
    snapshot_json,
    parent_method_name=None,
    parent_method_file_name=None
):
    parent_method_name = parent_method_name or inspect.stack()[1][3]
    parent_method_file_name = parent_method_file_name or inspect.stack()[1][1]

    file_name = "{}__{}.json".format(os.path.basename(parent_method_file_name), parent_method_name)
    snapshot_dir_path = os.path.join(os.path.dirname(parent_method_file_name), '__snapshots__')
    file_path = os.path.join(snapshot_dir_path, file_name)
    os.makedirs(snapshot_dir_path, exist_ok=True)
    if not os.path.isfile(file_path):
        generate_snapshot_file(snapshot_json, file_path, file_name)
        return False
    else:
        with open(file_path, "r") as snapshot_file:
            snapshot_file_contents = snapshot_file.read()
            new_snapshot_json = generate_json(snapshot_json)
            is_same_snapshot = new_snapshot_json == snapshot_file_contents
            if not is_same_snapshot:
                if os.environ.get('OVERRIDE_SNAPSHOTS', 'false') == 'true':
                    generate_snapshot_file(snapshot_json, file_path, file_name)
                    return True
                print("""snapshot got an unexpected result. Below is a diff of the old values that changed:
                \n{snashot_diff}
                \nBelow is the new, outputted json:
                \n{new_snapshot_json}
                """.format(
                    snashot_diff=generate_json(
                        diff(new_snapshot_json, snapshot_file_contents, load=True)),
                    new_snapshot_json=new_snapshot_json
                ))
            return is_same_snapshot
