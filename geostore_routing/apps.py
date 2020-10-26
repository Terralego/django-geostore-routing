from django.apps import AppConfig, apps
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import gettext_lazy as _

from geostore_routing.signals import feature_routing


class GeostoreConfig(AppConfig):
    name = 'geostore_routing'
    verbose_name = _("Routing plugin for Geographic Store")

    def ready(self):
        # Set specific classes to work with geostore
        # setattr(settings, 'GEOSTORE_LAYER_VIEWSSET', 'geostore_routing.views.LayerViewsSet')
        # setattr(settings, 'GEOSTORE_LAYER_SERIALIZER', 'geostore_routing.serializers.LayerSerializer')

        # add topology update signals
        post_save.connect(feature_routing, sender=apps.get_model('geostore.Feature'))
        pre_delete.connect(feature_routing, sender=apps.get_model('geostore.Feature'))
