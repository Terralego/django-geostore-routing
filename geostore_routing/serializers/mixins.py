from django.urls import reverse
from rest_framework import serializers


class RoutingLayerSerializerMixin(serializers.Serializer):
    routing_url = serializers.SerializerMethodField()

    def get_routing_url(self, obj):
        if obj.routable:
            return reverse('layer-route', args=[obj.pk, ])
