# -*- coding: utf-8 -*-

def parse(content):
    """
    :param content: A JSON API document already
    :returns: The JSON API document parsed
    """
    if "data" not in content:
        raise AttributeError("This is not a JSON API document")

    if isinstance(content["data"], dict):
        return _flat(content["data"])
    elif isinstance(content["data"], list):
        result = []
        for obj in content["data"]:
            result.append(_flat(obj))
        return result
    else:
        return None


def _flat(obj):
    if "attributes" in obj:
        obj.update(obj.pop("attributes"))
    return obj
