Routing API
=======

django-geostore-routing integrate a way to use your LineString layer as a routing one.

Arguments
^^^^^^^^^

First attribute needed, and mandatory, is ``geom``, it must contains a LineString from start to endpoint, passing through all
the way points. Geostore will create a path passing on the intersection the closest of those point, in the order you provided it.

It can also be provided a ``callbackid``, that is used to identify the request. It can be useful in async environment. The ``callbackid``
is provided «as is» in the response.

Query content can provided in a POST or a GET request.

An example of response:

.. code-block:: javascript

    {
        'request': {
            'callbackid': 'my_callback',
            'geom': {
                "type": 'LineString',
                "coordinates": [
                [
                    10.8984375,
                    52.1874047455997
                ],
                [
                    1.58203125,
                    46.042735653846506
                ]
                ]
            }
        },
        'geom': {
            'type': 'LineString',
            'coordinates': [
            [
                1.6259765625,
                45.767522962149876
            ],
            [
                5.2294921875,
                46.558860303117164
            ],
            [
                10.986328125,
                52.10650519075632
            ]
            ]
        },
        'route': {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        'type': 'LineString',
                        'coordinates': [
                        [
                            1.6259765625,
                            45.767522962149876
                        ],
                        [
                            5.2294921875,
                            46.558860303117164
                        ]
                        ]
                    },
                    "properties": {
                       "id": 1
                     },
                },
                {
                    "type": "Feature",
                    "geometry": {
                        'type': 'LineString',
                        'coordinates': [
                        [
                            5.2294921875,
                            46.558860303117164
                        ],
                        [
                            10.986328125,
                            52.10650519075632
                        ]
                        ]
                    },
                    "properties": {
                       "id": 2
                     },
                }
            ]
        }
    }

