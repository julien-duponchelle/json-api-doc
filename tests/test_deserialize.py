#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `json_api_doc` package."""

import json

import json_api_doc


def test_deserialize_is_non_destructive():
    raw_response = """
    {
        "jsonapi": {
            "version": "1.0"
        },
        "meta": {
            "foo": "bar"
        },
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
    """
    response = json.loads(raw_response)
    json_api_doc.deserialize(response)
    assert response == json.loads(raw_response)


def test_first_level_data_in_included():
    response = {
        "data": {
            "type": "article",
            "id": "1"
        },
        "included": [
            {
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
        ]
    }
    doc = json_api_doc.deserialize(response)
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
