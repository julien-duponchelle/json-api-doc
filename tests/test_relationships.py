from json_api_doc import json_api_doc


def test_flat():
    data = {
        "type": "article",
        "id": "1",
        "attributes": {
            "title": "Article 1"
        },
        "relationships": {
            "author": {
                "data": {"type": "people", "id": "9"}
            }
        }
    }
    assert json_api_doc._flat(data)["author"] == ("people", "9")


def test_parse_included():
    data = [{
        "type": "people",
        "id": "9",
        "attributes": {
            "first-name": "Bob",
            "last-name": "Doe",
            }
        }
    ]
    assert json_api_doc._parse_included(data) == {
        ("people", "9"): {
            "type": "people",
            "id": "9",
            "first-name": "Bob",
            "last-name": "Doe",
        }
    }


def test_resolve():
    included = {
        ("people", "9"): {
            "name": "Jean"
        }
    }
    data = {
        "title": "Article 1",
        "author": ("people", "9")
    }
    doc = json_api_doc._resolve(data, included)
    assert doc == {
        "title": "Article 1",
        "author": {"name": "Jean"}
    }


def test_simple_relationships():
    response = {
        "data": {
            "type": "article",
            "id": "1",
            "attributes": {
                "title": "Article 1"
            },
            "relationships": {
                "author": {
                    "data": {"type": "people", "id": "9"}
                }
            }
        },
        "included": [{
            "type": "people",
            "id": "9",
            "attributes": {
                "first-name": "Bob",
                "last-name": "Doe",
                }
            }
        ]
    }
    doc = json_api_doc.parse(response)
    assert doc == {
        "type": "article",
        "id": "1",
        "title": "Article 1",
        "author": {
            "type": "people",
            "id": "9",
            "first-name": "Bob",
            "last-name": "Doe"
        }
    }
