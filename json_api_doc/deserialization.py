import copy


def deserialize(content):
    """
    :param content: A JSON API document already
    :returns: The JSON API document parsed
    """
    if "errors" in content:
        return content

    if "data" not in content:
        raise AttributeError("This is not a JSON API document")

    # be nondestructive with provided content
    content = copy.deepcopy(content)

    if "included" in content:
        included = _parse_included(content["included"])
    else:
        included = {}
    if isinstance(content["data"], dict):
        return _resolve(_flat(content["data"]), included, set())
    elif isinstance(content["data"], list):
        result = []
        for obj in content["data"]:
            result.append(_resolve(_flat(obj), included, set()))
        return result
    else:
        return None


def _resolve(data, included, resolved):
    if set(data.keys()) == {"type", "id"}:
        type_id = data["type"], data["id"]
        resolved_item = included.get(type_id, data)
        if type_id in resolved:
            return data
        else:
            return _resolve(
                resolved_item,
                included,
                resolved | {type_id}
            )
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = _resolve(value, included, resolved)
        elif isinstance(value, list):
            data[key] = [
                _resolve(item, included, resolved)
                for item in value
            ]
        else:
            data[key] = value
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
            data = item.get("data")
            links = item.get("links")
            if data is not None:
                obj[relationship] = data
            elif links:
                obj[relationship] = item
            else:
                obj[relationship] = None
    return obj
