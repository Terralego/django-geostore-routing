from django.test import TestCase
from geostore import GeometryTypes
from geostore.models import Layer

from geostore_routing.serializers import LayerSerializer


class RoutingLayerSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.layer = Layer.objects.create(name='test_layer', geom_type=GeometryTypes.LineString, routable=True)

    def test_routing_url(self):
        serializer = LayerSerializer(self.layer)
        self.assertIn('routing_url', serializer.data)
