# -*- coding: utf-8 -*-


def parse(content):
    """
    :param content: A JSON API document already
    :returns: The JSON API document parsed
    """
    if "data" not in content:
        raise AttributeError("This is not a JSON API document")

    if "included" in content:
        included = _parse_included(content["included"])
    else:
        included = []
    if isinstance(content["data"], dict):
        return _resolve(_flat(content["data"]), included)
    elif isinstance(content["data"], list):
        result = []
        for obj in content["data"]:
            result.append(_resolve(_flat(obj), included))
        return result
    else:
        return None


def _resolve(data, included):
    for key, value in data.items():
        if isinstance(value, tuple):
            data[key] = included[value]
    return data


def _parse_included(included):
    result = {}
    for include in included:
        result[(include["type"], include["id"])] = _flat(include)
    return result


def _flat(obj):
    if "attributes" in obj:
        obj.update(obj.pop("attributes"))
    if "relationships" in obj:
        for relationship, item in obj.pop("relationships").items():
            obj[relationship] = (item["data"]["type"], item["data"]["id"])
    return obj
