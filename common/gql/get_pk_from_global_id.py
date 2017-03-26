from graphene.relay import Node


def get_pk_from_global_id(node_id):
    try:
        pk = Node.from_global_id(node_id)[1]
        if pk.isnumeric():
            return int(pk)
        return pk
    except:
        raise Exception('malformed id passed: {}'.format(node_id))
