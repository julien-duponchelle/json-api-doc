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


def _resolve(data, included, resolved, deep=True):
    if not isinstance(data, dict):
        return data
    keys = data.keys()
    if keys == {"type", "id"} or keys == {"type", "id", "meta"}:
        type_id = data["type"], data["id"]
        meta = data.get("meta")
        resolved_item = included.get(type_id, data)
        resolved_item = resolved_item.copy()
        if type_id not in resolved:
            data = _resolve(
                resolved_item,
                included,
                resolved | {type_id}
            )
        if meta is not None:
            data = data.copy()
            data.update(meta=meta)
        return data
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = _resolve(value, included, resolved)
        elif isinstance(value, list):
            if deep:
                data[key] = [
                    _resolve(item, included, resolved, False)
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
