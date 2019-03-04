# -*- coding: utf-8 -*-

__author__ = """Julien Duponchelle"""
__email__ = 'julien@duponchelle.info'
__version__ = '0.4.0'


def parse(content):
    """
    :param content: A JSON API document already
    :returns: The JSON API document parsed
    """
    if "errors" in content:
        return content

    if "data" not in content:
        raise AttributeError("This is not a JSON API document")

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

def encode(content):
    """
    :param content: Dict with data to be encoded
    :returns: JSONAPI encoded object
    """
    included = {}
    if isinstance(content, list):
        data = list(map(lambda l: _expand(l, included), content))
    else:
        data = _expand(content, included)

    res = {
        "data": data
    }

    if included:
        res["included"] = list(included.values())

    return res

def _expand(data, included):
    obj_type = data.get("$type", None)
    if obj_type == None:
        raise AttributeError("Missing object $type")

    attrs = {} 
    rels = {}
    for k, v in data.items():
        if k in ["$type", "id"]:
            continue

        if isinstance(v, dict):
            rel = _expand_included(v, included)
            rels[k] = {
                "data": rel
            }
        elif isinstance(v, list):
            rel = list(map(lambda l: _expand_included(l, included), v))
            rels[k] = {
                "data": rel
            }
        else:
            attrs[k] = v

    encoded = {
        "type": obj_type,
    }
    
    obj_id = data.get("id", None)
    
    if obj_id != None:
        encoded["id"] = obj_id 

    if len(attrs):
        encoded["attributes"] = attrs

    if len(rels):
        encoded["relationships"] = rels

    return encoded

def _expand_included(data, included):
    obj_type = data.get("$type", None)
    if obj_type == None:
        raise AttributeError("Missing object $type")

    obj_id = data.get("id", None)
    if obj_id == None:
        raise AttributeError("Missing object id")

    attrs = {} 
    rels = {}
    if (obj_type, obj_id) not in included:
        for k, v in data.items():
            if k in ["$type", "id"]:
                continue
            
            if isinstance(v, dict):
                rel = _expand_included(v, included)
                rels[k] = {
                    "data": rel
                }
            elif isinstance(v, list):
                rel = list(map(lambda l: _expand_included(l, included), v))
                rels[k] = {
                    "data": rel
                }
            else:
                attrs[k] = v

        encoded = {
            "type": obj_type,
            "id": obj_id 
        }

        if len(attrs):
            encoded["attributes"] = attrs

        if len(rels):
            encoded["relationships"] = rels

        included[(obj_type, obj_id)] = encoded
    
    return {
        "type": obj_type,
        "id": obj_id
    }
    

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
            if isinstance(data, list):
                obj[relationship] = [
                    (i["type"], i["id"]) for i in data
                ]
            elif data is None:
                obj[relationship] = None
            else:
                obj[relationship] = (data["type"], data["id"])
    return obj

if __name__ == "__main__":
    data = {
        "$type": "article",
        "id": "1",
        "title": "Article 1",
        "comments": [{
            "$type": "comment",
            "id": "100",
            "content": "First"
        },{
            "$type": "comment",
            "id": "101",
            "content": "Second"
        }]
    }
    res = encode(data)
    print(res)