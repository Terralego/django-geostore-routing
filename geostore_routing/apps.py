from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import gettext_lazy as _
from geostore.models import Feature

from geostore_routing.signals import feature_routing


class GeostoreConfig(AppConfig):
    name = 'geostore_routing'
    verbose_name = _("Routing plugin for Geographic Store")

    def ready(self):
        # Set specific classes to work with geostore
        settings.GEOSTORE_LAYER_VIEWSSET = 'geostore_routing.views.LayerViewSet'
        settings.GEOSTORE_LAYER_SERIALIZER = 'geostore_routing.serializers.LayerViewSet'
        # add topology update signals
        post_save.connect(feature_routing, sender=Feature)
        pre_delete.connect(feature_routing, sender=Feature)
