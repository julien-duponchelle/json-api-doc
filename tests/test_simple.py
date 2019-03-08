#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `json_api_doc` package."""

import pytest


import json_api_doc


def test_simple_null_object():
    response = {
        "data": None
    }
    doc = json_api_doc.parse(response)
    assert doc is None


def test_simple_object():
    response = {
        "data": {
            "type": "article",
            "id": "1",
            "attributes": {
                "title": "Article 1"
            },
        }
    }
    doc = json_api_doc.parse(response)
    assert doc == {
        "type": "article",
        "id": "1",
        "title": "Article 1"
    }


def test_simple_object_without_attributes():
    response = {
        "data": {
            "type": "article",
            "id": "1"
        }
    }
    doc = json_api_doc.parse(response)
    assert doc == {
        "type": "article",
        "id": "1"
    }


def test_simple_list():
    response = {
        "data": [
            {
                "type": "article",
                "id": "1",
                "attributes": {
                    "title": "Article 1"
                },
            },
            {
                "type": "article",
                "id": "2",
                "attributes": {
                    "title": "Article 2"
                },
            }
        ]
    }
    doc = json_api_doc.parse(response)
    assert len(doc) == 2
    assert doc[0] == {
        "type": "article",
        "id": "1",
        "title": "Article 1"
    }
    assert doc[1] == {
        "type": "article",
        "id": "2",
        "title": "Article 2"
    }


def test_invalid():
    with pytest.raises(AttributeError):
        json_api_doc.parse({"a": 1})


def test_error():
    response = {
        "errors":[{
            "status":"404",
            "title":"not found",
            "detail":"Resource not found"
        }]
    }
    doc = json_api_doc.parse(response)
    assert doc == response
