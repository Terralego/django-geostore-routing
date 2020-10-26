from django.conf import settings
from django.urls import reverse
from rest_framework import serializers


class RoutingLayerSerializer:
    routing_url = serializers.SerializerMethodField()

    def get_routing_url(self, obj):
        return reverse('layer-route', args=[obj.pk, ])
