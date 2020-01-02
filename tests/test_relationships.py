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
    assert json_api_doc._flat(data)["author"] == {"type": "people", "id": "9"}


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
        {"type": "people", "id": "9"},
        {"type": "people", "id": "10"}
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
        "author": {"type": "people", "id": "9"}
    }
    doc = json_api_doc._resolve(data, included, set())
    assert doc == {
        "title": "Article 1",
        "author": {"name": "Jean"}
    }


def test_resolve_with_meta():
    included = {
        ("people", "9"): {
            "name": "Jean"
        }
    }
    data = {
        "title": "Article 1",
        "author": {"type": "people", "id": "9", "meta": {"index": 3}}
    }
    doc = json_api_doc._resolve(data, included, set())
    assert doc == {
        "title": "Article 1",
        "author": {"name": "Jean", "meta": {"index": 3}}
    }


def test_resolve_missing():
    included = {
    }
    data = {
        "title": "Article 1",
        "author": {"type": "people", "id": "9"}
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
            {"type": "people", "id": "9"},
            {"type": "people", "id": "10"},
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


def test_resolve_list_with_meta():
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
            {"type": "people", "id": "9", "meta": {"index": 3}},
            {"type": "people", "id": "10", "meta": {"index": 18}},
        ]
    }
    doc = json_api_doc._resolve(data, included, set())
    assert doc == {
        "title": "Article 1",
        "authors": [
            {"name": "Jean", "meta": {"index": 3}},
            {"name": "Luc", "meta": {"index": 18}},
        ]
    }


def test_resolve_list_missing_items():
    included = {
    }
    data = {
        "title": "Article 1",
        "authors": [
            {"type": "people", "id": "9"},
            {"type": "people", "id": "10"},
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
            "address": {"type": "location", "id": "2"},
        },
        ("location", "2"): {
            "street": "boulevard magenta",
            "city": {"type": "city", "id": "3"}
        },
        ("city", "3"): {
            "name": "Paris"
        }
    }
    data = {
        "title": "Article 1",
        "author": {"type": "people", "id": "9"}
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
            "father": {"type": "people", "id": "2"},
        },
        ("people", "2"): {
            "name": "Luc",
            "son": {"type": "people", "id": "1"},
        },
    }
    data = {
        "title": "Article 1",
        "author": {"type": "people", "id": "1"}
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


def test_simple_relationships_with_meta():
    response = {
        "data": {
            "type": "article",
            "id": "1",
            "attributes": {
                "title": "Article 1"
            },
            "relationships": {
                "author": {
                    "data": {"type": "people", "id": "9", "meta": {"index": 3}}
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
            "last-name": "Doe",
            "meta": {"index": 3}
        }
    }


def test_linked_relationship():
    response = {
        "data": {
            "type": "article",
            "id": "1",
            "attributes": {
                "title": "Article 1"
            },
            "relationships": {
                "author": {
                    "links": {
                        "related": "/authors/9"
                    }
                }
            }
        }
    }
    doc = json_api_doc.parse(response)
    assert doc == {
        "type": "article",
        "id": "1",
        "title": "Article 1",
        "author": {
            "links": {
                "related": "/authors/9"
            }
        }
    }
