from django.db.models.signals import post_save, post_delete
from geostore.models import Feature

from geostore_routing.signals import feature_routing

# Register geostore_routing signals on geostore models
post_save.connect(feature_routing, sender=Feature)
post_delete.connect(feature_routing, sender=Feature)
