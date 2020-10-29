from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from geostore import settings as geostore_settings


class GeostoreRoutingConfig(AppConfig):
    name = 'geostore_routing'
    verbose_name = _("Routing plugin for Geographic Store")

    def ready(self):
        geostore_settings.GEOSTORE_LAYER_VIEWSSET = 'geostore_routing.views.LayerViewsSet'
        geostore_settings.GEOSTORE_LAYER_SERIALIZER = 'geostore_routing.serializers.LayerSerializer'

        import geostore_routing.signals.handlers  # NOQA
