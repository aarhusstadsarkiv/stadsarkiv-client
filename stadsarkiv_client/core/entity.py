def is_primitive(value):
    return isinstance(value, (str, int, float, bool))


def is_list(value):
    return isinstance(value, list)


def is_dict(value):
    return isinstance(value, dict)


def is_list_of_primitives(value):
    if not isinstance(value, list):
        return False
    for item in value:
        if not is_primitive(item):
            return False
    return True


def is_list_of_dicts(value):
    if not isinstance(value, list):
        return False
    for item in value:
        if not is_dict(item):
            return False
    return True