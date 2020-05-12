# -*- coding: utf-8 -*-

from collections import OrderedDict


def serialize(data={}, errors={}, meta={}, links={}):
    """
    :param data: Dict with data to serialize
    :param errors: Dict with error data to serialize
    :param meta: Dict with meta data to serialize
    :returns: Dict normalized as a valid JSON API document
    """

    if data and errors:
        raise AttributeError("""Only 'data' or 'errors' can be present in a
                                valid JSON API document""")

    included = OrderedDict()
    res = {}
    if data:
        if isinstance(data, list):
            res["data"] = list(
                map(lambda item: _serialize(item, included), data))
        else:
            res["data"] = _serialize(data, included)
    elif isinstance(data, list):
        res["data"] = []

    if included:
        res["included"] = list(included.values())

    if meta:
        res["meta"] = meta

    if errors:
        res["errors"] = errors

    if links:
        res["links"] = links

    return res or {"data": None}


def _serialize(data, included):
    obj_type = data.get("$type", None)
    if obj_type is None:
        raise AttributeError("Missing object $type")

    res = _expand(data, included)

    res["type"] = obj_type
    obj_id = data.get("id", None)
    if obj_id is not None:
        res["id"] = obj_id

    return res


def _expand(data, included):
    res = {}
    attrs = {}
    rels = {}
    for k, v in data.items():
        if k in ["$type", "id"]:
            continue

        if isinstance(v, dict):
            embedded, is_res = _expand_included(v, included)
            if is_res:
                rels[k] = {
                    "data": embedded
                }
            else:
                attrs[k] = embedded
        elif isinstance(v, list):
            embedded = list(map(lambda l: _expand_included(l, included), v))
            if all(map(lambda i: i[1], embedded)):
                rels[k] = {
                    "data": list(map(lambda i: i[0], embedded))
                }
            else:
                attrs[k] = list(map(lambda i: i[0], embedded))
        else:
            attrs[k] = v

    if len(attrs):
        res["attributes"] = attrs

    if len(rels):
        res["relationships"] = rels

    return res


def _expand_included(data, included):
    if not isinstance(data, dict):
        return data, False

    typ = data.get("$type", None)
    id = data.get("id", None)

    if typ is None or id is None:
        # not a sub-resource, return as is
        return data, False

    if typ is not None and id is not None and (typ, id) not in included:
        serialized = _expand(data, included)
        serialized["type"] = typ
        serialized["id"] = id
        included[(typ, id)] = serialized

    return {"type": typ, "id": id}, True
