Settings
========

GEOSTORE_ROUTING_CELERY_ASYNC
-----------------------------
**Default: False**

Boolean that activate automatic topology update in celery worker. Use only if a celery working is activated and configured for your project.
Until, use update_topology command


GEOSTORE_ROUTING_TOLERANCE
--------------------------
**Default: 0.000001**

Tolerance to snap geometries in topologies. This default value match with INTERNAL_GEOMETRY_SRID unit (default WGS84 4326, angles)
