=====
Usage
=====

To use JSON API doc in a project::

    import json_api_doc

The module provides 2 functions, serialize and deserialize.

To transform the JSON API document into a simple denormalized Python dict use
`deserialize`:

.. code-block:: python

    document =  {
        'data': {
            'type': 'article,
            'id': '1',
            'attributes': {
                'name': 'Article 1'
            }
        }
    }
    json_api_doc.deserialize(document)

To transform the a Python dict object into a normalized JSON API document use
`serialize`:

.. code-block:: python

    obj =  {
        '$type': 'article,
        'id': '1',
        'name': 'Article 1'
    }
    json_api_doc.serialize(document)


.. automodule:: json_api_doc
    :members:
    :undoc-members:
