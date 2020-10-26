from celery import shared_task
from django.apps import apps

from geostore_routing import settings as app_settings
from .helpers import Routing


@shared_task
def feature_update_routing(layer_id, ewkt):
    """ Update all feature topologies """
    Layer = apps.get_model('geostore.Layer')  # use lazy models because tasks are loaded by signals in apps.ready()
    layer = Layer.objects.get(pk=layer_id)
    if layer.routable:
        features = layer.features.filter(geom__dwithin=(ewkt,
                                                        app_settings.GEOSTORE_ROUTING_TOLERANCE)
                                         ).values_list('pk', flat=True)
        Routing.update_topology(layer, features)
    return True
