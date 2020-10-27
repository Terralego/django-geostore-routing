from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geostore', '0043_merge_20201023_1209'),
    ]

    operations = [
        migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS pgrouting")
    ]
