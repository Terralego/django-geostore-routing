Installation
============

Requirements
------------

DATABASE
^^^^^^^^

Minimum configuration :
 * Python 3.6+
 * PostgreSQL 10+
 * PostGIS 2.4+
 * PgRouting 2.5+

Recommended configuration :
 * Python 3.8
 * PostgreSQL 12
 * PostGIS 3
 * PgRouting 3

Your final django project should use django.contrib.gis.backend.postgis as default DATABASE backend


USING docker image :

Prebuilt docker image builded by makinacorpus

https://hub.docker.com/r/makinacorpus/pgrouting

SYSTEM REQUIREMENTS
^^^^^^^^^^^^^^^^^^^

these are debian packages required

- libpq-dev   (psycopg2)
- gettext     (translations)
- binutils    (django.contrib.gis)
- libproj-dev (django.contrib.gis)
- gdal-bin    (django.contrib.gis)

recommended

- postgresql-client (if you want to use ./manage.py dbshell command)

With pip
--------

From Pypi:

::

    pip install django-geostore-routing

From Github:

::

    pip install -e https://github.com/Terralego/django-geostore-routing.git@master#egg=django-geostore-routing

With git
--------

::

    git clone https://github.com/Terralego/django-geostore-routing.git
    cd django-geostore-routing
    python setup.py install


In your project settings
------------------------

.. code-block:: python

  INSTALLED_APPS = (
    ...
    "geostore",
    "geostore_routing",
    ...
  )

Settings up
-----------

pgRouting needs to update a table that contains all linestring to create topological connections.
You need to execute a command to create topology at first.
Once, after every feature update topology will be automatically updated if you enable GEOSTORE_ROUTING_CELERY_ASYNC with a working celery worker.
