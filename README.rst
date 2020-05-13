============
JSON API Doc
============


.. image:: https://img.shields.io/pypi/v/json-api-doc.svg
        :target: https://pypi.python.org/pypi/json-api-doc

.. image:: https://img.shields.io/travis/noplay/json-api-doc.svg
        :target: https://travis-ci.org/noplay/json-api-doc

.. image:: https://readthedocs.org/projects/json-api-doc/badge/?version=latest
        :target: https://json-api-doc.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/noplay/json-api-doc/shield.svg
     :target: https://pyup.io/repos/github/noplay/json-api-doc/
     :alt: Updates



This library provides ability to transform between normalized JSON API
(http://jsonapi.org/) documents and denormalized Python dictionary object for
easier manipulation in code.
Also available as a command line utility and Python 3 module.

Deserialization
~~~~~~~~~~~~~~~

For this JSON API document:

.. code-block:: json

    {
      "data": [{
        "type": "articles",
        "id": "1",
        "attributes": {
          "title": "JSON API paints my bikeshed!",
          "body": "The shortest article. Ever.",
          "created": "2015-05-22T14:56:29.000Z",
          "updated": "2015-05-22T14:56:28.000Z"
        },
        "relationships": {
          "author": {
            "data": {"id": "42", "type": "people"}
          }
        }
      }],
      "included": [
        {
          "type": "people",
          "id": "42",
          "attributes": {
            "name": "John",
            "age": 80,
            "gender": "male"
          }
        }
      ]
    }

The simplified version will be:

.. code-block:: json

    [
        {
            "type": "articles",
            "id": "1",
            "title": "JSON API paints my bikeshed!",
            "body": "The shortest article. Ever.",
            "created": "2015-05-22T14:56:29.000Z",
            "updated": "2015-05-22T14:56:28.000Z",
            "author": {
                "type": "people",
                "id": "42",
                "name": "John",
                "age": 80,
                "gender": "male"
            }
        }
    ]

Serialization
~~~~~~~~~~~~~

To turn an dict into JSON API specification document the root of your object
must contain a `$type` key with a value corresponding to the name of
the object's resource type. Any sub-dict or sub-array of dicts that also
contain a `$type` key will be considered an included documents and serialized
accordingly.

.. code-block:: json

    [
        {
            "$type": "articles",
            "id": "1",
            "title": "JSON API paints my bikeshed!",
            "body": "The shortest article. Ever.",
            "created": "2015-05-22T14:56:29.000Z",
            "updated": "2015-05-22T14:56:28.000Z",
            "author": {
                "$type": "people",
                "id": "42",
                "name": "John",
                "age": 80,
                "gender": "male"
            }
        }
    ]

.. code-block:: json

    {
      "data": [{
        "type": "articles",
        "id": "1",
        "attributes": {
          "title": "JSON API paints my bikeshed!",
          "body": "The shortest article. Ever.",
          "created": "2015-05-22T14:56:29.000Z",
          "updated": "2015-05-22T14:56:28.000Z"
        },
        "relationships": {
          "author": {
            "data": {"id": "42", "type": "people"}
          }
        }
      }],
      "included": [
        {
          "type": "people",
          "id": "42",
          "attributes": {
            "name": "John",
            "age": 80,
            "gender": "male"
          }
        }
      ]
    }

Usage as python module
----------------------

.. code-block:: python

        import json_api_doc

        document =  {
            'data': {
                'type': 'article',
                'id': '1',
                'attributes': {
                    'name': 'Article 1'
                }
            }
        }
        json_api_doc.deserialize(document)

.. code-block:: python

        import json_api_doc

        document =  {
          '$type': 'article',
          'id': '1',
          'name': 'Article 1'
        }
        json_api_doc.serialize(document)

Usage as cli
------------

.. code-block:: bash

    $ jsonapidoc document.json


Contributors
-------------
* Julien Duponchelle (https://github.com/noplay)
* Antonio Martinović (https://github.com/TopHatCroat)
* Jeff Zellman (https://github.com/jzellman)
* Brenda Deely (https://github.com/brendadeely)
* Taylor Hobbs (https://github.com/TayHobbs)

Licence
--------
Free software: Apache Software License 2.0

Documentation
--------------
Full Documentation is available: https://json-api-doc.readthedocs.io.

