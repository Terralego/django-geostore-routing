from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, tag
from geostore import GeometryTypes
from geostore.models import Layer
from geostore.tests.factories import LayerFactory

from geostore_routing.tests.utils import get_files_tests


@tag("routing")
class UpdateTopologyTestCase(TestCase):
    def test_update_topology_routing_fail(self):
        layer = LayerFactory(geom_type=GeometryTypes.Point)
        with self.assertRaises(CommandError) as error:
            call_command(
                'update_topology',
                f'--layer-pk={layer.pk}',
                verbosity=0)
        self.assertEqual('An error occuring during topology update', str(error.exception))

    def test_update_topology_fail(self):
        output = StringIO()
        with self.assertRaises(CommandError) as error:
            call_command(
                'update_topology',
                '--layer-pk=999',
                verbosity=0, stdout=output)
        self.assertEqual("Layer with pk 999 doesn't exist", str(error.exception))

    def test_update_topology(self):
        geojson = get_files_tests('toulouse.geojson')

        call_command(
            'import_geojson',
            f'{geojson}',
            verbosity=0)

        # Retrieve the layer
        in_layer = Layer.objects.first()

        output = StringIO()
        call_command(
            'update_topology',
            f'--layer-pk={in_layer.pk}',
            '--tolerance=0.0001',
            verbosity=1, stdout=output)
        self.assertIn('Topology successfully updated', output.getvalue())
