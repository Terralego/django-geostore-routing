from geostore.views import LayerViewSet as BaseLayerViewsSet

from geostore_routing.views.mixins import RoutingViewsSetMixin


class LayerViewsSet(RoutingViewsSetMixin, BaseLayerViewsSet):
    pass
