from django.contrib.gis.geos import LineString, Point
from django.db import connection
from django.test import TestCase
from django.urls import reverse
import json
from geostore import GeometryTypes
from geostore.models import Feature, Layer
from geostore.tests.factories import FeatureFactory, UserFactory
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from geostore_routing import settings as app_settings
from geostore_routing.helpers import Routing, RoutingException
from geostore_routing.tests.utils import get_files_tests


class RoutingTestCase(TestCase):
    points = [
        {
            "type": "Point",
            "coordinates": [
                1,
                43
            ]
        }, {
            "type": "Point",
            "coordinates": [
                1.5,
                43.5
            ]
        }
    ]

    points_second_line = [
        {
            "type": "Point",
            "coordinates": [
                1.6,
                43.6
            ]
        }, {
            "type": "Point",
            "coordinates": [
                2,
                44
            ]
        }
    ]

    out_points = [
        {
            "type": "Point",
            "coordinates": [
                1.001,
                43
            ]
        }, {
            "type": "Point",
            "coordinates": [
                1.499,
                43.5
            ]
        },
        {
            "type": "Point",
            "coordinates": [
                2.001,
                44.000
            ]
        }
    ]

    @classmethod
    def setUpTestData(cls):
        cls.layer = Layer.objects.create(name='test_layer', geom_type=GeometryTypes.LineString, routable=True)
        cls.user = UserFactory(is_superuser=True)
        cls.point_1 = Point(cls.points[0]["coordinates"])
        cls.point_2 = Point(cls.points[1]["coordinates"])

        cls.out_point_1 = Point(cls.out_points[0]["coordinates"])
        cls.out_point_2 = Point(cls.out_points[1]["coordinates"])
        cls.out_point_3 = Point(cls.out_points[2]["coordinates"])

        cls.point_second_line_1 = Point(cls.points_second_line[0]["coordinates"])
        cls.point_second_line_2 = Point(cls.points_second_line[1]["coordinates"])

        cls.feature = FeatureFactory.create(geom=LineString([cls.point_1, cls.point_2]), layer=cls.layer)
        cls.feature_2 = FeatureFactory.create(geom=LineString([cls.point_second_line_1,
                                                               cls.point_second_line_2]), layer=cls.layer)
        Routing.update_topology(cls.layer, tolerance=0.0001)

    def setUp(self):
        self.client.force_login(self.user)

    def test_routing_view_no_routes_found(self):
        geometry = LineString([self.out_point_1, self.out_point_3], srid=app_settings.INTERNAL_GEOMETRY_SRID)
        response = self.client.post(reverse('layer-route',
                                            args=[self.layer.pk]),
                                    {'geom': geometry.geojson, })
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_routing_view_waypoints(self):
        geometry = LineString([self.out_point_2, self.out_point_1], srid=app_settings.INTERNAL_GEOMETRY_SRID)
        response = self.client.post(reverse('layer-route',
                                            args=[self.layer.pk]),
                                    {'geom': geometry.geojson, })
        self.assertEqual(HTTP_200_OK, response.status_code)
        response = response.json()

        self.assertAlmostEqual(response['waypoints'][0]['coordinates'][0], 1.4995)
        self.assertAlmostEqual(response['waypoints'][0]['coordinates'][1], 43.4995)
        self.assertAlmostEqual(response['waypoints'][1]['coordinates'][0], 1.0005)
        self.assertAlmostEqual(response['waypoints'][1]['coordinates'][1], 43.0005)

        self.assertEqual(response['way'], json.loads(LineString([1.0005, 43.0005], [1.4995, 43.4995],
                                                                srid=app_settings.INTERNAL_GEOMETRY_SRID).geojson))

    def test_routing_view_opposite_order_waypoints(self):
        geometry = LineString([self.out_point_1, self.out_point_2], srid=app_settings.INTERNAL_GEOMETRY_SRID)
        response = self.client.post(reverse('layer-route',
                                            args=[self.layer.pk]),
                                    {'geom': geometry.geojson, })
        self.assertEqual(HTTP_200_OK, response.status_code)
        response = response.json()

        self.assertAlmostEqual(response['waypoints'][1]['coordinates'][0], 1.4995)
        self.assertAlmostEqual(response['waypoints'][1]['coordinates'][1], 43.4995)
        self.assertAlmostEqual(response['waypoints'][0]['coordinates'][0], 1.0005)
        self.assertAlmostEqual(response['waypoints'][0]['coordinates'][1], 43.0005)

        self.assertEqual(response['way'], json.loads(LineString([1.0005, 43.0005], [1.4995, 43.4995],
                                                                srid=app_settings.INTERNAL_GEOMETRY_SRID).geojson))


class ComplexRoutingTestCase(TestCase):
    points = [
        {
            "type": "Point",
            "coordinates": [
                1.4534568786621094,
                43.622127847162005
            ]
        }, {
            "type": "Point",
            "coordinates": [
                1.4556884765625,
                43.61839973326468
            ]
        }, {
            "type": "Point",
            "coordinates": [
                1.4647650718688965,
                43.61916090863259
            ]
        }
    ]

    @classmethod
    def setUpTestData(cls):
        cls.layer = Layer.objects.create(name='test_layer', geom_type=GeometryTypes.LineString, routable=True)
        cls.user = UserFactory(is_superuser=True)

        geojson_path = get_files_tests('toulouse.geojson')

        with open(geojson_path,
                  mode='r',
                  encoding="utf-8") as geojson:
            cls.layer.from_geojson(geojson.read())

        Routing.update_topology(cls.layer, tolerance=0.0001)

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_points_in_line(self):
        routing = Routing(
            [Point(*p['coordinates'],
                   srid=app_settings.INTERNAL_GEOMETRY_SRID) for p in self.points
             ],
            self.layer)

        self.assertIsInstance(routing.get_route(), dict)

    def test_routing_view_bad_geometry(self):
        response = self.client.post(reverse('layer-route',
                                            args=[self.layer.pk]))

        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code, response.json())

        bad_geometry = Point((1, 1))
        response = self.client.post(reverse('layer-route',
                                            args=[self.layer.pk]),
                                    {'geom': bad_geometry.geojson, })
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)

    def test_routing_view(self):
        points = [Point(
            *point['coordinates'],
            srid=app_settings.INTERNAL_GEOMETRY_SRID) for point in self.points]

        geometry = LineString(*points)

        response = self.client.post(reverse('layer-route',
                                            args=[self.layer.pk]),
                                    {'geom': geometry.geojson, })

        self.assertEqual(HTTP_200_OK, response.status_code)
        response = response.json()

        self.assertEqual(response.get('route').get('type'), 'FeatureCollection')
        self.assertTrue(len(response.get('route').get('features')) >= 2)

        # Ensure End Points are close to requested points
        start = Point(*response.get('route').get('features')[0].get('geometry')
                      .get('coordinates')[0])
        end = Point(*response.get('route').get('features')[-1].get('geometry')
                    .get('coordinates')[-1])
        self.assertTrue(points[0].distance(start) <= 0.001)
        self.assertTrue(points[-1].distance(end) <= 0.001)

        self.assertEqual(len(response.get('waypoints')), 2)
        first_distance = response.get('waypoints')[0].get('distance')
        third_distance = response.get('waypoints')[1].get('distance')
        self.assertEqual(first_distance, 12.0)
        self.assertEqual(third_distance, 6.82)

    def test_routing_view_edge_case(self):
        points = [Point(
            *p['coordinates'],
            srid=app_settings.INTERNAL_GEOMETRY_SRID) for p in
            [self.points[0], self.points[0]]]

        geometry = LineString(*points)

        response = self.client.post(reverse('layer-route',
                                            args=[self.layer.pk]),
                                    {'geom': geometry.geojson, })
        self.assertEqual(HTTP_200_OK, response.status_code)
        response = response.json()
        self.assertEqual(response.get('route').get('type'), 'FeatureCollection')
        self.assertTrue(len(response.get('route').get('features')) >= 1)

        # Ensure End Points are close to requested points
        start = Point(*response.get('route').get('features')[0].get('geometry')
                      .get('coordinates'))
        end = Point(*response.get('route').get('features')[-1].get('geometry')
                    .get('coordinates'))
        self.assertTrue(points[0].distance(start) <= 0.001)
        self.assertTrue(points[-1].distance(end) <= 0.001)

    def test_routing_cache(self):
        geometry = LineString(*[Point(
            *point['coordinates'],
            srid=app_settings.INTERNAL_GEOMETRY_SRID) for point in self.points])
        with self.settings(DEBUG=True,
                           CACHES={'default': {
                               'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}
                           }):

            self.client.post(reverse('layer-route',
                                     args=[self.layer.pk]),
                             {'geom': geometry.geojson, })

            initial_count = len(connection.queries)
            counts = []
            for x in range(2):
                self.client.post(
                    reverse('layer-route', args=[self.layer.pk]),
                    {'geom': geometry.geojson, }
                )

                counts.append(len(connection.queries))

            self.assertTrue(all([counts[0] == c for c in counts]))
            self.assertTrue(all([initial_count > c for c in counts]))

    def test_layer_with_polygon(self):
        """test that a layer with another kind of geometry raise the right exception"""
        feature = FeatureFactory()

        with self.assertRaises(RoutingException):
            Routing(self.points, feature.layer)

    def test_routing_view_with_polygon(self):
        """test that a layer with another kind of geometry raise the right exception"""
        feature = FeatureFactory()

        points = [Point(
            *p['coordinates'],
            srid=app_settings.INTERNAL_GEOMETRY_SRID) for p in
            [self.points[0], self.points[0]]]

        geometry = LineString(*points)

        response = self.client.post(reverse('layer-route',
                                            args=[feature.layer.pk]),
                                    {'geom': geometry.geojson, })
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)
        error = response.json()['errors'][0]
        self.assertEqual("Layer is not routable", error)


class UpdateTopologyTestCase(TestCase):
    points = [Point(0, 40, srid=app_settings.INTERNAL_GEOMETRY_SRID),
              Point(10, 40, srid=app_settings.INTERNAL_GEOMETRY_SRID)]

    def setUp(self):
        self.layer = Layer.objects.create(name='test_layer', routable=True)
        self.user = UserFactory(is_superuser=True)
        self.client.force_login(self.user)
        self.other_feature = Feature.objects.create(layer=self.layer, geom="SRID=4326;LINESTRING(5 40, 6 40)")
        self.feature1 = Feature.objects.create(layer=self.layer, geom="SRID=4326;LINESTRING(0 40, 1 40)")
        self.feature2 = Feature.objects.create(layer=self.layer, geom="SRID=4326;LINESTRING(1 40, 9 40)")
        self.feature3 = Feature.objects.create(layer=self.layer, geom="SRID=4326;LINESTRING(9 40, 10 40)")
        self.feature4 = Feature.objects.create(layer=self.layer, geom="SRID=4326;LINESTRING(1 40, 1 41, 9 41, 9 40)")
        self.assertTrue(Routing.update_topology(self.layer, tolerance=0.0001))

    def test_remove_geom_update_routing(self):
        geometry = LineString(self.points, srid=app_settings.INTERNAL_GEOMETRY_SRID)
        old_response = self.client.post(reverse('layer-route',
                                                args=[self.layer.pk]),
                                        {'geom': geometry.geojson})
        self.assertEqual(HTTP_200_OK, old_response.status_code)
        old_json = old_response.json()
        old_features = old_json.get('route').get('features')
        first_id = self.feature3.pk
        id_new_features = [feature['properties']['id'] for feature in old_features]
        self.assertIn(first_id, id_new_features)

        self.feature3.delete()

        new_response = self.client.post(reverse('layer-route',
                                                args=[self.layer.pk]),
                                        {'geom': geometry.geojson})
        self.assertEqual(HTTP_200_OK, new_response.status_code, new_response)
        new_json = new_response.json()
        self.assertNotEqual(old_json, new_json)
        id_new_features = [feature['properties']['id'] for feature in new_json.get('route').get('features')]
        self.assertNotIn(first_id, id_new_features)
        self.assertNotIn(self.other_feature.pk, id_new_features)

    def test_update_geom_update_routing(self):
        geometry = LineString(self.points, srid=app_settings.INTERNAL_GEOMETRY_SRID)
        old_response = self.client.post(reverse('layer-route',
                                                args=[self.layer.pk]),
                                        {'geom': geometry.geojson})
        self.assertEqual(HTTP_200_OK, old_response.status_code)
        old_json = old_response.json()
        old_features = old_json.get('route').get('features')
        first_id = self.feature3.pk
        id_new_features = [feature['properties']['id'] for feature in old_features]
        self.assertIn(first_id, id_new_features)

        self.feature3.geom = LineString((1, 40), (1, 38), (9, 38), (9, 40))
        self.feature3.save()

        new_response = self.client.post(reverse('layer-route',
                                                args=[self.layer.pk]),
                                        {'geom': geometry.geojson})
        self.assertEqual(HTTP_200_OK, new_response.status_code)
        new_json = new_response.json()
        self.assertNotEqual(old_json, new_json)
        id_new_features = [feature['properties']['id'] for feature in new_json.get('route').get('features')]
        self.assertNotIn(first_id, id_new_features)
        self.assertNotIn(self.other_feature.pk, id_new_features)
