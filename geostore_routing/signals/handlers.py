from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from geostore.models import Feature
from geostore.helpers import execute_async_func

from geostore_routing import settings as app_settings
from geostore_routing.tasks import feature_update_routing


@receiver(post_save, sender=Feature)
@receiver(post_delete, sender=Feature)
def update_topologies_near_feature(sender, instance, **kwargs):
    """ Launch topology updates near feature on routable layers """
    if instance.layer.routable:
        args = (instance.layer_id,
                instance.geom.ewkt)
        execute_async_func(feature_update_routing,
                           args)\
            if app_settings.GEOSTORE_ROUTING_CELERY_ASYNC \
            else feature_update_routing(*args)
