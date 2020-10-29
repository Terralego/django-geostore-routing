from django.contrib.gis.geos import LineString
from django.utils.translation import gettext as _
from geostore import settings as app_settings
from geostore.serializers import LayerSerializer as BaseLayerSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_gis import serializers as geo_serializers

from geostore_routing.serializers.mixins import RoutingLayerSerializerMixin


class RoutingSerializer(serializers.Serializer):
    geom = geo_serializers.GeometryField(help_text=_("A linestring with ordered waypoints."))
    callback_id = serializers.CharField(required=False, help_text=_("Optional callback id to match with your request."))
    route = serializers.JSONField(read_only=True, help_text=_("All features used, in geojson format."))
    way = geo_serializers.GeometryField(read_only=True, help_text=_("Routed way, as Linestring."), precision=6)

    def validate_geom(self, value):
        if not isinstance(value, LineString):
            raise ValidationError(_("Geometry should be a LineString object."))
        value.srid = app_settings.INTERNAL_GEOMETRY_SRID
        return value


class LayerSerializer(RoutingLayerSerializerMixin, BaseLayerSerializer):
    pass
