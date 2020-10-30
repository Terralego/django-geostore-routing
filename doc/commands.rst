Commands
--------

update_topology
===============

.. code-block:: bash

  ./manage.py update_topology -pk <layer_pk> --tolerance <tolerance>

You must provide the pk of the layer you want to use.
Tolerance for extremity snapping is 0.00001 by default (unity should match to your INTERNAL_GEOMETRY_SRID, by default for 4326 see https://www.usna.edu/Users/oceano/pguth/md_help/html/approx_equivalents.htm )
