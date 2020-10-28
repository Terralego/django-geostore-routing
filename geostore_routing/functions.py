from django.contrib.gis.db.models import GeometryField
from django.contrib.gis.db.models.functions import GeoFunc


class LineSubstring(GeoFunc):
    output_field = GeometryField()
