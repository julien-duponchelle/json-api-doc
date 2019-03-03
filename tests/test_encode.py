#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `json_api_doc` package."""

import pytest

import json_api_doc


def test_encode_object():
    data = {
        "$type": "article",
        "id": "1",
        "title": "Article 1"
    }
    doc = json_api_doc.encode(data)
    assert doc == {
        "data": {
            "type": "article",
            "id": "1",
            "attributes": {
                "title": "Article 1"
            }
        }
    }


def test_encode_object_list():
    data = [{
        "$type": "article",
        "id": "1",
        "title": "Article 1"
    }, {
        "$type": "article",
        "id": "2",
        "title": "Article 2"
    }]

    doc = json_api_doc.encode(data)
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


def test_encode_object_without_attributes():
    data = {
        "$type": "article",
        "id": "1"
    }
    doc = json_api_doc.encode(data)
    assert doc == {
        "data": {
            "type": "article",
            "id": "1"
        }
    }


def test_invalid():
    with pytest.raises(AttributeError):
        json_api_doc.parse({"a": 1})


def test_encode_object_embedded():
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
    doc = json_api_doc.encode(data)
    assert doc == {
        "data": {
            "type": "article",
            "id": "1",
            "attributes": {
                "title": "Article 1"
            },
            "relationships": {
                "author": {
                    "data": { "type": "people", "id": "9" }
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


def test_encode_object_embedded_list():
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
    doc = json_api_doc.encode(data)
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
                        { "type": "comment", "id": "100" },
                        { "type": "comment", "id": "101" }
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
        },{
            "type": "comment",
            "id": "101",
            "attributes": {
                "content": "Second",
            }
        }]
    }
