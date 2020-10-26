from django.conf import settings
from geostore.settings import *  # NOQA

GEOSTORE_ROUTING_CELERY_ASYNC = getattr(settings, 'GEOSTORE_ROUTING_CELERY_ASYNC', False)
GEOSTORE_ROUTING_TOLERANCE = getattr(settings, 'GEOSTORE_ROUTING_TOLERANCE', 0.000001)
