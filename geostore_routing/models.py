from django.db.models.signals import post_save, post_delete
from geostore.models import Feature
from geostore.signals import execute_async_func

from geostore_routing import settings as app_settings
from geostore_routing.tasks import feature_update_routing


def update_topologies_near_feature(sender, instance, **kwargs):
    """ Launch topology updates near feature on linestring layers """
    if app_settings.GEOSTORE_ROUTING_CELERY_ASYNC and instance.layer.is_linestring:
        execute_async_func(feature_update_routing,
                           (instance.layer_id, instance.geom.ewkt))


# Signal registration
# update topologies on creation / update
post_save.connect(update_topologies_near_feature, sender=Feature)
# update topologies on deletion
post_delete.connect(update_topologies_near_feature, sender=Feature)
