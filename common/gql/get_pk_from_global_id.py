from common.relay import Node
from common.utils.deep_transform import deep_transform


def convert_input_global_ids_to_pks(input, id_keys=[]):
    def condition(key, val):
        return key and '_id' in key or key in id_keys

    def transform(key, val):
        return get_pk_from_global_id(val)

    return deep_transform(input, condition, transform)


def get_pk_from_global_id(node_id):
    try:
        pk = Node.from_global_id(node_id)[1]
        if pk.isnumeric():
            return int(pk)
        return pk
    except:
        raise Exception('malformed id passed: {}'.format(node_id))
