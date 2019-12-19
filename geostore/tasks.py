from celery import shared_task
from django.apps import apps


@shared_task
def feature_update_relations_destinations(feature_id):
    Feature = apps.get_model('geostore.Feature')
    feature = Feature.objects.get(pk=feature_id)
    feature.sync_relations()


@shared_task
def layer_relations_set_destinations(relation_id):
    LayerRelation = apps.get_model('geostore.LayerRelation')
    try:
        relation = LayerRelation.objects.get(pk=relation_id)
    except LayerRelation.DoesNotExist:
        raise Exception('DoesNotExists', relation_id, LayerRelation)
    for feature in relation.origin.features.all():
        feature.sync_relations(relation_id)
