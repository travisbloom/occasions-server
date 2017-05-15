def deep_transform(input, condition, transformation):
    def convert_dict(key, val):
        if isinstance(val, dict):
            return {key: convert_dict(key, val) for key, val, in val.items()}
        if isinstance(val, list):
            return [convert_dict(key, val) for val in val]
        if condition(key, val):
            return transformation(key, val)
        return val
    return convert_dict(None, input)
