import json_api_doc


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


def test_flat_list():
    data = {
        "type": "article",
        "id": "1",
        "attributes": {
            "title": "Article 1"
        },
        "relationships": {
            "authors": {
                "data": [
                    {"type": "people", "id": "9"},
                    {"type": "people", "id": "10"}
                ]
            }
        }
    }
    assert json_api_doc._flat(data)["authors"] == [
        ("people", "9"),
        ("people", "10")
    ]


def test_flat_none():
    data = {
        "type": "article",
        "id": "1",
        "attributes": {
            "title": "Article 1"
        },
        "relationships": {
            "authors": {
                "data": None
            }
        }
    }
    assert json_api_doc._flat(data)["authors"] is None


def test_parse_included():
    data = [{
        "type": "people",
        "id": "9",
        "attributes": {
            "first-name": "Bob",
            "last-name": "Doe",
        }
    }]
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
    doc = json_api_doc._resolve(data, included, set())
    assert doc == {
        "title": "Article 1",
        "author": {"name": "Jean"}
    }


def test_resolve_missing():
    included = {
    }
    data = {
        "title": "Article 1",
        "author": ("people", "9")
    }
    doc = json_api_doc._resolve(data, included, set())
    assert doc == {
        "title": "Article 1",
        "author": {"type": "people", "id": "9"}
    }


def test_resolve_list():
    included = {
        ("people", "9"): {
            "name": "Jean"
        },
        ("people", "10"): {
            "name": "Luc"
        }
    }
    data = {
        "title": "Article 1",
        "authors": [
            ("people", "9"),
            ("people", "10"),
        ]
    }
    doc = json_api_doc._resolve(data, included, set())
    assert doc == {
        "title": "Article 1",
        "authors": [
            {"name": "Jean"},
            {"name": "Luc"},
        ]
    }


def test_resolve_list_missing_items():
    included = {
    }
    data = {
        "title": "Article 1",
        "authors": [
            ("people", "9"),
            ("people", "10"),
        ]
    }
    doc = json_api_doc._resolve(data, included, set())
    assert doc == {
        "title": "Article 1",
        "authors": [
            {"id": "9", "type": "people"},
            {"id": "10", "type": "people"}
        ]
    }


def test_resolve_nested():
    included = {
        ("people", "9"): {
            "name": "Jean",
            "address": ("location", "2"),
        },
        ("location", "2"): {
            "street": "boulevard magenta",
            "city": ("city", "3")
        },
        ("city", "3"): {
            "name": "Paris"
        }
    }
    data = {
        "title": "Article 1",
        "author": ("people", "9")
    }
    doc = json_api_doc._resolve(data, included, set())
    assert doc == {
        "title": "Article 1",
        "author": {
            "name": "Jean",
            "address": {
                "street": "boulevard magenta",
                "city": {"name": "Paris"}
            }
        }
    }


def test_resolve_loop():
    included = {
        ("people", "1"): {
            "name": "Jean",
            "father": ("people", "2"),
        },
        ("people", "2"): {
            "name": "Luc",
            "son": ("people", "1"),
        },
    }
    data = {
        "title": "Article 1",
        "author": ("people", "1")
    }
    doc = json_api_doc._resolve(data, included, set())
    assert doc == {
        "title": "Article 1",
        "author": {
            "name": "Jean",
            "father": {
                "name": "Luc",
                "son": {"type": "people", "id": "1"}
            }
        }
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
        }]
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
