=====
Usage
=====

To use JSON API doc in a project::

    import json_api_doc

The main function is parse:

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
    json_api_doc.parse(document)


.. automodule:: json_api_doc
    :members:
    :undoc-members:
