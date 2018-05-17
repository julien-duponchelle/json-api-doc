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
            resolved = included.get(value, {
                "type": value[0],
                "id": value[1]
            })
            data[key] = _resolve(resolved, included)
        elif isinstance(value, list):
            l = []
            for item in value:
                if isinstance(item, tuple):
                    resolved = included.get(item, {
                        "type": item[0],
                        "id": item[1]
                    })
                    l.append(_resolve(resolved, included))
                else:
                    l.append(item)
            data[key] = l
    return data


def _parse_included(included):
    result = {}
    for include in included:
        result[(include["type"], include["id"])] = _flat(include)
    return result


def _flat(obj):
    obj.pop("links", None)
    obj.update(obj.pop("attributes", {}))
    if "relationships" in obj:
        for relationship, item in obj.pop("relationships").items():
            if isinstance(item["data"], list):
                obj[relationship] = [
                    (i["type"], i["id"]) for i in item["data"]
                ]
            elif item["data"] is None:
                obj[relationship] = None
            else:
                obj[relationship] = (item["data"]["type"], item["data"]["id"])
    return obj
