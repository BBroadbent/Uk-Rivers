# Generated by Django 4.0 on 2022-01-03 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guidebook', '0002_remove_river_get_in_remove_river_get_out_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='river',
            name='geojson',
        ),
        migrations.RemoveField(
            model_name='river',
            name='get_in_geojson',
        ),
        migrations.RemoveField(
            model_name='river',
            name='get_out_geojson',
        ),
        migrations.RemoveField(
            model_name='river',
            name='river_description',
        ),
        migrations.RemoveField(
            model_name='river',
            name='river_name',
        ),
    ]
