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
    for key, value in data.items():
        if isinstance(value, tuple):
            id = {
                "type": value[0],
                "id": value[1]
            }
            resolved_item = included.get(value, id)

            if value in resolved:
                data[key] = id
            else:
                data[key] = _resolve(
                    resolved_item,
                    included,
                    resolved | set((value, ))
                )
        elif isinstance(value, list):
            l = []
            for item in value:
                if isinstance(item, tuple):
                    id = {
                        "type": item[0],
                        "id": item[1]
                    }
                    resolved_item = included.get(item, id)
                    if item in resolved:
                        data[key] = id
                    else:
                        l.append(
                            _resolve(
                                resolved_item,
                                included, resolved | set((item, )))
                        )
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
            data = item.get("data")
            links = item.get("links")
            if isinstance(data, list):
                obj[relationship] = [
                    (i["type"], i["id"]) for i in data
                ]
            elif data is None and links:
                obj[relationship] = item
            elif data is None and links is None:
                obj[relationship] = None
            else:
                obj[relationship] = (data["type"], data["id"])
    return obj
