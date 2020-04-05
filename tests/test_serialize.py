#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `json_api_doc` package."""

import pytest

import json_api_doc


def test_serialize_object():
    data = {
        "$type": "article",
        "id": "1",
        "title": "Article 1"
    }
    doc = json_api_doc.serialize(data)
    assert doc == {
        "data": {
            "type": "article",
            "id": "1",
            "attributes": {
                "title": "Article 1"
            }
        }
    }


def test_serialize_object_list():
    data = [{
        "$type": "article",
        "id": "1",
        "title": "Article 1"
    }, {
        "$type": "article",
        "id": "2",
        "title": "Article 2"
    }]

    doc = json_api_doc.serialize(data)
    assert doc == {
        "data": [{
            "type": "article",
            "id": "1",
            "attributes": {
                "title": "Article 1"
            }
        }, {
            "type": "article",
            "id": "2",
            "attributes": {
                "title": "Article 2"
            }
        }]
    }

def test_serialize_empty_list():
    doc = json_api_doc.serialize([])
    assert doc == {
        "data": []
    }


def test_serialize_object_without_attributes():
    data = {
        "$type": "article",
        "id": "1"
    }
    doc = json_api_doc.serialize(data)
    assert doc == {
        "data": {
            "type": "article",
            "id": "1"
        }
    }


def test_invalid():
    with pytest.raises(AttributeError):
        json_api_doc.serialize({"a": 1})


def test_serialize_object_embedded():
    data = {
        "$type": "article",
        "id": "1",
        "title": "Article 1",
        "author": {
            "$type": "people",
            "id": "9",
            "name": "Bob"
        }
    }
    doc = json_api_doc.serialize(data)
    assert doc == {
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
                "name": "Bob",
            }
        }]
    }


def test_serialize_object_embedded_list():
    data = {
        "$type": "article",
        "id": "1",
        "title": "Article 1",
        "comments": [{
            "$type": "comment",
            "id": "100",
            "content": "First"
        }, {
            "$type": "comment",
            "id": "101",
            "content": "Second"
        }]
    }
    doc = json_api_doc.serialize(data)
    assert doc == {
        "data": {
            "type": "article",
            "id": "1",
            "attributes": {
                "title": "Article 1"
            },
            "relationships": {
                "comments": {
                    "data": [
                        {"type": "comment", "id": "100"},
                        {"type": "comment", "id": "101"}
                    ]
                }
            }
        },
        "included": [{
            "type": "comment",
            "id": "100",
            "attributes": {
                "content": "First",
            }
        }, {
            "type": "comment",
            "id": "101",
            "attributes": {
                "content": "Second",
            }
        }]
    }


def test_serialize_object_embedded_json():
    data = {
        "$type": "article",
        "id": "1",
        "title": "Article 1",
        "author": {
            "$type": "people",
            "id": "100"
        },
        "inner": {
            "value": "embedded regular JSON"
        },
        "innerArray": [
            "embedded", "regular", "JSON", "array"
        ],
        "innerObjectArray": [
            {
                "value": "something"
            }, {
                "value": "something_else"
            }
        ]
    }
    doc = json_api_doc.serialize(data)
    assert doc == {
        "data": {
            "type": "article",
            "id": "1",
            "attributes": {
                "title": "Article 1",
                "inner": {
                    "value": "embedded regular JSON"
                },
                "innerArray": [
                    "embedded", "regular", "JSON", "array"
                ],
                "innerObjectArray": [
                    {
                        "value": "something"
                    }, {
                        "value": "something_else"
                    }
                ]
            },
            "relationships": {
                "author": {
                    "data": {
                        "type": "people",
                        "id": "100"
                    }
                }
            }
        },
        "included": [{
            "type": "people",
            "id": "100"
        }]
    }


def test_serialize_meta():
    meta = {
        "some": "random",
        "silly": "data"
    }
    doc = json_api_doc.serialize(meta=meta)
    assert doc == {
        "meta": {
            "some": "random",
            "silly": "data"
        }
    }


def test_serialize_errors():
    errors = {
        "some": "random",
        "silly": "data"
    }
    doc = json_api_doc.serialize(errors=errors)
    assert doc == {
        "errors": {
            "some": "random",
            "silly": "data"
        }
    }


def test_serialize_links():
    links = {
        "some": "random",
        "silly": {
            "href": "random",
            "meta": {
                "silly": "data"
            }
        }
    }
    doc = json_api_doc.serialize(links=links)
    assert doc == {
        "links": {
            "some": "random",
            "silly": {
                "href": "random",
                "meta": {
                    "silly": "data"
                }
            }
        }
    }


def test_serialize_object_deep():
    data = {
        "$type": "article",
        "id": "1",
        "title": "Article 1",
        "author": {
            "$type": "people",
            "id": "10",
            "name": "Bob",
            "role": {
                "$type": "role",
                "id": "100",
                "name": "Writer"
            }
        }
    }
    doc = json_api_doc.serialize(data)
    assert doc == {
        "data": {
            "type": "article",
            "id": "1",
            "attributes": {
                "title": "Article 1"
            },
            "relationships": {
                "author": {
                    "data": {
                        "type": "people",
                        "id": "10"
                    }
                }
            }
        },
        "included": [
            {
                "type": "role",
                "id": "100",
                "attributes": {
                    "name": "Writer",
                }
            }, {
                "type": "people",
                "id": "10",
                "attributes": {
                    "name": "Bob",
                },
                "relationships": {
                    "role": {
                        "data": {
                            "type": "role",
                            "id": "100"
                        }
                    }
                }
            }
        ]
    }


def test_error_and_data():
    with pytest.raises(AttributeError):
        doc = {
            "data": {
                "$type": "article"
            },
            "errors": {
                "status": 200
            }
        }
        json_api_doc.serialize(**doc)
