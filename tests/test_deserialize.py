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

def test_can_handle_deep_recursive_relationships():
    response = {
        'data': {
            'type': 'Version',
            'id': '1',
            'attributes': {},
            'relationships': {
                'drivers': {
                    'meta': {'count': 1},
                    'data': [{'type': 'Driver', 'id': '1'}]
                },
                'named_insureds': {
                    'meta': {'count': 1},
                    'data': [{'type': 'NamedInsured', 'id': '1'}]
                },
                'losses': {
                    'meta': {'count': 1},
                    'data': [{'type': 'Loss', 'id': '1'}]
                },
            }
        },
        'included': [
            {
                'type': 'Address',
                'id': '1',
                'attributes': {},
                'relationships':
                    {
                        'entities': {
                            'meta': {'count': 1},
                            'data': [{'type': 'Entity', 'id': '1'}]
                        },
                        'info': {
                            'meta': {'count': 1},
                            'data': [{'type': 'AddressInfo', 'id': '1'}]
                        }
                    }
            }, {
                'type': 'AddressInfo',
                'id': '1',
                'attributes': {},
                'relationships': {
                    'address': {
                        'data': {'type': 'Address', 'id': '1'}
                    }
                }
            }, {
                'type': 'Driver',
                'id': '1',
                'attributes': {},
                'relationships': {
                    'entity': {
                        'data': {'type': 'Entity', 'id': '1'}
                    }
                }
            }, {
                'type': 'Entity',
                'id': '1',
                'attributes': {},
                'relationships': {
                    'addresses': {
                        'meta': {'count': 1},
                        'data': [{'type': 'Address', 'id': '1'}]
                    }
                }
            }, {
                'type': 'Loss',
                'id': '1',
                'attributes': {},
                'relationships': {
                    'address': {
                        'data': {'type': 'Address', 'id': '1'}
                    },
                }
            }, {
                'type': 'NamedInsured',
                'id': '1',
                'attributes': {},
                'relationships': {
                    'entity': {
                        'data': {'type': 'Entity', 'id': '1'}
                    }
                }
            },
        ]
    }
    doc = json_api_doc.deserialize(response)
    assert bool(doc["drivers"][0]["entity"]["addresses"][0]["info"]) is True
    assert bool(doc["losses"][0]["address"]) is True
