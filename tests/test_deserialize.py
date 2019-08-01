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
