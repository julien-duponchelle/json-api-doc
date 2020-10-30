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
        "data": {
            "type": "Version",
            "id": "1",
            "attributes": {},
            "relationships": {
                "drivers": {
                    "meta": {"count": 1},
                    "data": [{"type": "Driver", "id": "1"}]
                },
                "named_insureds": {
                    "meta": {"count": 1},
                    "data": [{"type": "NamedInsured", "id": "1"}]
                },
                "losses": {
                    "meta": {"count": 1},
                    "data": [{"type": "Loss", "id": "1"}]
                },
            }
        },
        "included": [
            {
                "type": "Address",
                "id": "1",
                "attributes": {},
                "relationships":
                    {
                        "entities": {
                            "meta": {"count": 1},
                            "data": [{"type": "Entity", "id": "1"}]
                        },
                        "info": {
                            "meta": {"count": 1},
                            "data": [{"type": "AddressInfo", "id": "1"}]
                        }
                }
            }, {
                "type": "AddressInfo",
                "id": "1",
                "attributes": {},
                "relationships": {
                    "address": {
                        "data": {"type": "Address", "id": "1"}
                    }
                }
            }, {
                "type": "Driver",
                "id": "1",
                "attributes": {},
                "relationships": {
                    "entity": {
                        "data": {"type": "Entity", "id": "1"}
                    }
                }
            }, {
                "type": "Entity",
                "id": "1",
                "attributes": {},
                "relationships": {
                    "addresses": {
                        "meta": {"count": 1},
                        "data": [{"type": "Address", "id": "1"}]
                    }
                }
            }, {
                "type": "Loss",
                "id": "1",
                "attributes": {},
                "relationships": {
                    "address": {
                        "data": {"type": "Address", "id": "1"}
                    },
                }
            }, {
                "type": "NamedInsured",
                "id": "1",
                "attributes": {},
                "relationships": {
                    "entity": {
                        "data": {"type": "Entity", "id": "1"}
                    }
                }
            },
        ]
    }
    doc = json_api_doc.deserialize(response)
    assert bool(doc["drivers"][0]["entity"]["addresses"][0]["info"]) is True
    assert bool(doc["losses"][0]["address"]) is True


def test_resolves_deeply_without_infinite_recursion():
    response = {
        "data": [
            {
                "id": "O-546755D4",
                "relationships": {
                    "route": {
                        "data": {
                            "id": "Orange",
                            "type": "route"
                        }
                    },
                    "trip": {
                        "data": {
                            "id": "45616458",
                            "type": "trip"
                        }
                    }
                },
                "type": "vehicle"
            },
            {
                "id": "O-546751D5",
                "relationships": {
                    "route": {
                        "data": {
                            "id": "Orange",
                            "type": "route"
                        }
                    },
                    "trip": {
                        "data": {
                            "id": "45616586",
                            "type": "trip"
                        }
                    }
                },
                "type": "vehicle"
            },
            {
                "id": "O-54675162",
                "relationships": {
                    "route": {
                        "data": {
                            "id": "Orange",
                            "type": "route"
                        }
                    },
                    "trip": {
                        "data": {
                            "id": "45616587",
                            "type": "trip"
                        }
                    }
                },
                "type": "vehicle"
            }
        ],
        "included": [
            {
                "id": "45616586",
                "relationships": {
                    "route": {
                        "data": {
                            "id": "Orange",
                            "type": "route"
                        }
                    },
                    "route_pattern": {
                        "data": {
                            "id": "Orange-3-1",
                            "type": "route_pattern"
                        }
                    }
                },
                "type": "trip"
            },
            {
                "id": "Orange-3-1",
                "relationships": {
                    "token_trip": {
                        "data": {
                            "id": "45616458",
                            "type": "trip"
                        }
                    },
                    "route": {
                        "data": {
                            "id": "Orange",
                            "type": "route"
                        }
                    }
                },
                "type": "route_pattern"
            },
            {
                "id": "45616458",
                "relationships": {
                    "route": {
                        "data": {
                            "id": "Orange",
                            "type": "route"
                        }
                    },
                    "route_pattern": {
                        "data": {
                            "id": "Orange-3-1",
                            "type": "route_pattern"
                        }
                    }
                },
                "type": "trip"
            },
            {
                "id": "45616587",
                "relationships": {
                    "route": {
                        "data": {
                            "id": "Orange",
                            "type": "route"
                        }
                    },
                    "route_pattern": {
                        "data": {
                            "id": "Orange-3-1",
                            "type": "route_pattern"
                        }
                    }
                },
                "type": "trip"
            }
        ]
    }

    doc = json_api_doc.parse(response)
    trip_id = {'id': '45616458', 'type': 'trip'}
    route_id = {'id': 'Orange',
                'type': 'route'}
    route_pattern_id = {'id': 'Orange-3-1',
                        'type': 'route_pattern'}

    trip0 = doc[0]['trip']
    trip1 = doc[1]['trip']
    assert bool(trip0 != trip_id)
    assert bool(trip0['route_pattern']['route'] == route_id)
    assert bool(trip0['route_pattern']['token_trip'] == trip_id)

    assert bool(trip1['route_pattern'] != route_pattern_id)
    assert bool(trip1['route_pattern']['route'] == route_id)
    assert bool(trip1['route_pattern']['token_trip']['route'] == route_id)
    assert bool(trip1['route_pattern']['token_trip']['route_pattern'] == route_pattern_id)
