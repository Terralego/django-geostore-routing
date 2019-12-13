# Generated by Django 3.0 on 2019-12-13 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geostore', '0040_merge_20191213_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='featurerelation',
            name='relation',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_features', to='geostore.LayerRelation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='featurerelation',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_as_destination', to='geostore.Feature'),
        ),
        migrations.AlterField(
            model_name='featurerelation',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_as_origin', to='geostore.Feature'),
        ),
    ]
